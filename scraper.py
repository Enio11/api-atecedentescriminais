from playwright.async_api import async_playwright
import logging
import re
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def search_degree(page, url, document, degree_name):
    """
    Helper function to search a specific degree (1st or 2nd).
    """
    try:
        # Clean document (keep only numbers)
        clean_document = "".join(filter(str.isdigit, document))
        logger.info(
            f"Navigating to TJSP {degree_name} for document: {document} "
            f"(cleaned: {clean_document})"
        )
        await page.goto(url, timeout=60000)

        # Select "Documento da Parte" in the dropdown
        await page.select_option("select#cbPesquisa", value="DOCPARTE")

        # Wait for the input field to be visible
        await page.wait_for_selector("input#campo_DOCPARTE")

        # Fill the document
        await page.fill("input#campo_DOCPARTE", clean_document)

        # Click Search
        # Button ID might differ between degrees
        if "cposg" in url:  # 2nd Degree
            await page.click("input#pbConsultar")
        else:  # 1st Degree
            await page.click("input#botaoConsultarProcessos")

        # Wait for results or "no results" message
        try:
            await page.wait_for_load_state("networkidle", timeout=20000)
        except Exception:
            # Capture screenshot for debugging
            await page.screenshot(path=f"error_screenshot_{degree_name}.png")
            logger.warning(
                f"Timeout waiting for networkidle in {degree_name}. "
                f"Saved error_screenshot_{degree_name}.png"
            )
            pass

        # Check for "No results" message
        content = await page.content()
        if (
            "Não existem processos" in content
            or "Nenhum processo foi encontrado" in content
            or "Não existem informações disponíveis para os parâmetros informados" in content
        ):
            logger.info(f"No records found in {degree_name}.")
            return {"count": 0, "details": [], "names": []}

        # Check if we were redirected to a specific process detail page
        # This happens when there is only one result
        single_process_element = await page.query_selector("span#numeroProcesso")
        if single_process_element:
            proc_num = (await single_process_element.inner_text()).strip()
            logger.info(f"Redirected to detail page for process {proc_num} in {degree_name}")

            # Extract full details from the page
            full_details = await extract_details_from_page(page)

            # Extract names from parties list for the top-level names list
            found_names = set()
            for parte in full_details.get("partes", []):
                # parte string is like "Reqte: Name"
                parts = parte.split(":")
                if len(parts) > 1:
                    found_names.add(parts[1].strip())

            return {
                "count": 1,
                "details": [
                    {
                        "number": proc_num,
                        "degree": degree_name,
                        "link": page.url,
                        **full_details,  # Unpack all extracted details
                    }
                ],
                "names": list(found_names),
            }

        # Extract process items
        process_items = await page.query_selector_all(
            "div.processoDetalhes, tr.fundoClaro, tr.fundoEscuro"
        )

        count = 0
        details = []
        found_names = set()

        if not process_items:
            # Fallback to counting links
            process_links = await page.query_selector_all("a.linkProcesso")
            count = len(process_links)
            for link in process_links:
                text = await link.inner_text()
                href = await link.get_attribute("href")
                full_link = f"https://esaj.tjsp.jus.br{href}" if href else ""
                details.append({"number": text.strip(), "degree": degree_name, "link": full_link})
        else:
            count = len(process_items)
            for item in process_items:
                # Extract process number
                link = await item.query_selector("a.linkProcesso")
                if link:
                    proc_num = (await link.inner_text()).strip()
                    href = await link.get_attribute("href")
                    full_link = f"https://esaj.tjsp.jus.br{href}" if href else ""
                    details.append(
                        {"number": proc_num, "degree": degree_name, "link": full_link}
                    )

                # Extract text to find names
                text = await item.inner_text()
                lines = text.split("\n")
                for line in lines:
                    line = line.strip()
                    prefixes = [
                        "Reqte:",
                        "Reqdo:",
                        "Autor:",
                        "Réu:",
                        "Exectdo:",
                        "Exequente:",
                        "Agravante:",
                        "Agravado:",
                        "Averiguado:",
                        "Indiciado:",
                        "Requerente:",
                        "Requerido:",
                        "Impetrante:",
                        "Impetrado:",
                        "Interessado:",
                        "Embargante:",
                        "Embargado:",
                        "Apelante:",
                        "Apelado:",
                    ]
                    for prefix in prefixes:
                        if prefix.lower() in line.lower():
                            parts = re.split(f"{prefix}", line, flags=re.IGNORECASE)
                            if len(parts) > 1:
                                name_part = parts[1].strip()
                                if name_part:
                                    # Clean up common suffixes
                                    name_part = name_part.split("Advogado:")[0].strip()
                                    found_names.add(name_part)

        # Fallback: If process_items were found but no details were extracted
        if not details and count > 0:
            logger.warning(
                f"Process items found ({count}) but no details extracted. "
                "Trying direct link extraction."
            )
            process_links = await page.query_selector_all("a.linkProcesso")
            if process_links:
                count = len(process_links)  # Update count to match links
                for link in process_links:
                    text = await link.inner_text()
                    href = await link.get_attribute("href")
                    full_link = f"https://esaj.tjsp.jus.br{href}" if href else ""
                    details.append(
                        {"number": text.strip(), "degree": degree_name, "link": full_link}
                    )

        logger.info(f"Found {count} records in {degree_name}. Names: {list(found_names)}")
        return {"count": count, "details": details, "names": list(found_names)}

    except Exception as e:
        logger.error(f"Error during scraping {degree_name}: {e}")
        return {"error": str(e), "count": 0, "details": [], "names": []}


async def extract_details_from_page(page):
    """
    Extracts full details from a process detail page.
    """
    details = {}

    # Helper to get text safely
    async def get_text(selector):
        try:
            el = await page.query_selector(selector)
            return (await el.inner_text()).strip() if el else None
        except Exception:
            return None

    details["classe"] = await get_text("span#classeProcesso")
    details["area"] = await get_text("div#areaProcesso")
    details["assunto"] = await get_text("span#assuntoProcesso")
    details["data_distribuicao"] = await get_text("div#dataHoraDistribuicaoProcesso")
    details["juiz"] = await get_text("span#juizProcesso")
    details["valor_acao"] = await get_text("div#valorAcaoProcesso")

    # Extract Parties
    parties = []
    try:
        table_parts = await page.query_selector("table#tablePartesPrincipais")
        if table_parts:
            rows = await table_parts.query_selector_all("tr")
            for row in rows:
                # Usually 2 columns: Type (Reqte/Reqdo) and Name
                cols = await row.query_selector_all("td")
                if len(cols) >= 2:
                    type_text = (await cols[0].inner_text()).strip()
                    # Name often has extra whitespace or newlines
                    name_text = (await cols[1].inner_text()).replace("\n", " ").strip()
                    # Clean up name (remove "Advogado: ...")
                    name_clean = name_text.split("Advogado:")[0].strip()
                    parties.append(f"{type_text} {name_clean}")
    except Exception as e:
        logger.warning(f"Error extracting parties: {e}")
    details["partes"] = parties

    # Extract Movements (latest 5)
    movements = []
    try:
        table_moves = await page.query_selector("tbody#tabelaTodasMovimentacoes")
        if table_moves:
            rows = await table_moves.query_selector_all("tr")
            for i, row in enumerate(rows):
                if i >= 5:
                    break  # Limit to 5
                cols = await row.query_selector_all("td")
                if len(cols) >= 3:
                    date = (await cols[0].inner_text()).strip()
                    desc_raw = (await cols[2].inner_text()).strip()
                    # Clean up excessive whitespace/newlines
                    # Replace multiple newlines/tabs with a single newline
                    desc_clean = re.sub(r"\n\s*", "\n", desc_raw)
                    # Remove multiple spaces
                    desc_clean = re.sub(r" +", " ", desc_clean)
                    movements.append(f"{date} - {desc_clean}")
    except Exception as e:
        logger.warning(f"Error extracting movements: {e}")
    details["movimentacoes"] = movements

    return details


async def search_portal_transparencia(document: str):
    """
    Searches for person data on Portal da Transparência by CPF.
    Returns Name and Location.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use a standard User-Agent to avoid blocking
        user_agent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()

        try:
            # Clean document (keep only numbers)
            clean_document = "".join(filter(str.isdigit, document))
            logger.info(
                f"Navigating to Portal da Transparência for document: {document} "
                f"(cleaned: {clean_document})"
            )

            # Correct URL based on subagent findings
            await page.goto(
                "https://portaldatransparencia.gov.br/busca/",
                timeout=60000,
                wait_until="domcontentloaded",
            )

            # Wait for search box or search button
            # Sometimes the search box is hidden behind a button
            try:
                await page.wait_for_selector("button.bt-search", timeout=5000)
                await page.click("button.bt-search")
            except Exception:
                pass  # Button might not exist or be needed

            # Wait for search box
            await page.wait_for_selector("input#termo", timeout=20000)

            # Type CPF
            await page.fill("input#termo", clean_document)
            # await page.wait_for_timeout(500) # Removed for performance

            # Click Search Button explicitly
            # The button is inside the form
            search_btn = await page.query_selector("form#form-busca button[type='submit']")
            if search_btn:
                await search_btn.click()
            else:
                await page.press("input#termo", "Enter")

            # Wait for results
            # The result usually appears in a box "Resultado da busca"
            try:
                # Wait for at least one item in results (it's a div, not li)
                await page.wait_for_selector(
                    "ul#resultados div.busca-portal-block-searchs__item", timeout=20000
                )
            except Exception:
                logger.warning("Timeout waiting for results items.")

            # Check if any result is found
            # Wait a bit for dynamic load - replaced networkidle with specific selector wait above
            # await page.wait_for_load_state("networkidle")

            # Try to click the first result link
            # Get the link element
            link_element = await page.query_selector(
                "ul#resultados div.busca-portal-block-searchs__item a"
            )

            if not link_element:
                logger.info("No results found on Portal da Transparência.")
                return {"found": False, "name": None, "location": None}

            # Extract Name from the link text first (it's usually there)
            # Text: "Pessoa Física: ***.104.236-** - MICHELLE FARIA DE OLIVEIRA"
            link_text = await link_element.inner_text()
            name = None
            if "-" in link_text:
                name = link_text.split("-")[-1].strip()

            # Get href to navigate to details for Location
            href = await link_element.get_attribute("href")
            if href:
                # Construct absolute URL to avoid relative path issues
                # href is likely "busca/pessoa-fisica/..."
                # Base is "https://portaldatransparencia.gov.br/"
                if not href.startswith("/"):
                    href = "/" + href

                # If href starts with /busca/ and we are at /busca/,
                # it might be fine if we use root domain
                target_url = f"https://portaldatransparencia.gov.br{href}"
                logger.info(f"Navigating to detail page: {target_url}")

                await page.goto(target_url, timeout=60000, wait_until="domcontentloaded")

                # Extract Location from detail page
                # We need to find where "Localidade" is.
                # Usually in a definition list or similar.
                # We'll search the body text for "Localidade"
                content_text = await page.inner_text("body")

                # Regex for Location
                # "Localidade\nSÃO PAULO"
                loc_match = re.search(r"Localidade\s*\n\s*(.+)", content_text)
                location = None
                if loc_match:
                    location = loc_match.group(1).strip()

            return {
                "found": True,
                "name": name,
                "location": location,
                "source": "Portal da Transparência",
            }

        except Exception as e:
            logger.error(f"Error scraping Portal da Transparência: {e}")
            return {"error": str(e)}
        finally:
            await browser.close()


async def search_tjsp(document: str):
    """
    Searches for criminal records on TJSP eSAJ (1st and 2nd Degree) by CPF/CNPJ.
    Returns aggregated results.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Run searches concurrently
        page1 = await browser.new_page()
        page2 = await browser.new_page()

        task1 = search_degree(
            page1, "https://esaj.tjsp.jus.br/cpopg/open.do", document, "1º Grau"
        )
        task2 = search_degree(
            page2, "https://esaj.tjsp.jus.br/cposg/open.do", document, "2º Grau"
        )

        results = await asyncio.gather(task1, task2)

        await browser.close()

        # Aggregate results
        total_count = 0
        all_details = []
        all_names = set()
        errors = []

        for res in results:
            if "error" in res and res["error"]:
                errors.append(res["error"])

            total_count += res.get("count", 0)
            all_details.extend(res.get("details", []))
            all_names.update(res.get("names", []))

        final_result = {"count": total_count, "details": all_details, "names": list(all_names)}

        if errors:
            final_result["errors"] = errors

        return final_result
