import os
import pdfplumber
import csv
import re

def consolidate_pdfs(source_dir, output_file):
    pdf_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.pdf')]
    pdf_files.sort()
    
    all_data = []
    headers = ["Date", "Description", "Cost"]
    all_data.append(headers)
    
    print(f"Found {len(pdf_files)} PDF files in {source_dir}")

    for filename in pdf_files:
        filepath = os.path.join(source_dir, filename)
        print(f"Processing {filename}...")
        
        try:
            with pdfplumber.open(filepath) as pdf:
                if len(pdf.pages) < 3:
                    print(f"  Skipping {filename}: Less than 3 pages")
                    continue
                
                page = pdf.pages[2] # Page 3 (0-indexed)
                text = page.extract_text()
                
                lines = text.split('\n')
                
                found_purchases = False
                in_purchase_section = False
                
                for line in lines:
                    clean_line = line.strip()
                    
                    # Detect start of PURCHASE section
                    if clean_line == "PURCHASE":
                        in_purchase_section = True
                        continue
                    
                    # Detect end of section
                    if "Totals Year-to-Date" in clean_line or "INTEREST CHARGES" in clean_line:
                        in_purchase_section = False
                        
                    if not in_purchase_section:
                        continue

                    # Regex to match lines starting with MM/DD followed by description and ending with a number
                    # Example: 05/17 H-E-B #455 SAN MARCOS TX 5.93
                    match = re.match(r'^(\d{2}/\d{2})\s+(.+?)\s+(-?[\d,]+\.\d{2})$', clean_line)
                    
                    if match:
                        date = match.group(1)
                        description = match.group(2)
                        cost = match.group(3)
                        
                        # Exclude lines that might match but are not purchases
                        if not description.strip():
                            continue
                            
                        all_data.append([date, description, cost])
                        found_purchases = True
                
                if found_purchases:
                    print(f"  Found purchases in text.")
                else:
                    print(f"  No purchases found in text on page 3 of {filename}")


        except Exception as e:
            print(f"  Error processing {filename}: {e}")

    if len(all_data) <= 1:
        print("No data found to consolidate.")
        return

    # Generate CSV
    print(f"Generating {output_file} with {len(all_data)-1} rows...")
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(all_data)
        print("Done.")
    except Exception as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    consolidate_pdfs("data/pdfs", "consolidated_purchases.csv")
