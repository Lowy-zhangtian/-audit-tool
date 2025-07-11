# data_processing/data_cleaner.py
import pandas as pd
import re

class DataCleaner:
    def __init__(self):
        pass

    def clean_ocr_text(self, text):
        """Cleans raw OCR text: removes extra spaces, corrects common OCR errors (placeholder)."""
        print(f"Cleaning OCR text: {text[:50]}...")
        # Example: Remove multiple spaces
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        # Add more specific cleaning rules here based on observed OCR errors
        # e.g., correcting 'I' to '1', 'O' to '0' in certain contexts
        return cleaned_text

    def standardize_supplier_name(self, name):
        """Standardizes supplier names using a predefined mapping or rules."""
        # Example: "ABC Co." -> "ABC Company Inc."
        # This could involve a dictionary lookup or more complex string matching
        standardized_name = name.upper().replace("CO.", "COMPANY").replace("LTD.", "LIMITED")
        print(f"Standardizing supplier name: '{name}' -> '{standardized_name}'")
        return standardized_name

    def standardize_summary(self, summary_text):
        """Standardizes voucher summary descriptions."""
        # Example: "Purchase of office supplies" -> "OFFICE SUPPLIES PURCHASE"
        standardized_summary = summary_text.upper()
        print(f"Standardizing summary: '{summary_text}' -> '{standardized_summary}'")
        return standardized_summary

    def integrate_data(self, structured_data_df, ocr_extracted_fields_list):
        """Integrates structured ERP data with OCR extracted fields.
        Args:
            structured_data_df (pd.DataFrame): DataFrame from ERP.
            ocr_extracted_fields_list (list of dict): List of dictionaries, where each dict
                                                     contains key fields extracted from one document/image.
        Returns:
            pd.DataFrame: An integrated DataFrame with all voucher information.
        """
        print("Integrating structured data with OCR results...")
        # This is a simplified integration. Real-world integration might involve:
        # - Matching OCR data to ERP records (e.g., by voucher number, date, amount)
        # - Handling multiple attachments per ERP record
        # - Merging based on common identifiers

        # For this example, let's assume ocr_extracted_fields_list corresponds row-wise to structured_data_df
        # or we are creating new records from OCR data if no direct match.

        if structured_data_df is None and not ocr_extracted_fields_list:
            print("No data to integrate.")
            return pd.DataFrame()

        if ocr_extracted_fields_list:
            ocr_df = pd.DataFrame(ocr_extracted_fields_list)
            # Standardize columns from OCR if needed, e.g., amount to float
            if 'amount' in ocr_df.columns:
                ocr_df['amount'] = pd.to_numeric(ocr_df['amount'], errors='coerce')
            if 'tax_amount' in ocr_df.columns:
                ocr_df['tax_amount'] = pd.to_numeric(ocr_df['tax_amount'], errors='coerce')

            if structured_data_df is not None and not structured_data_df.empty:
                # Example: Concatenate or merge. For simplicity, let's try to concatenate if columns are similar
                # or add OCR fields as new columns if there's a key to join on.
                # This part needs a clear strategy based on data structure.
                # Assuming we want to add OCR fields as new columns to existing ERP data (if matched)
                # or append as new rows if they are independent.

                # Simplistic: if same number of rows, assume direct correspondence and join
                if len(structured_data_df) == len(ocr_df):
                    integrated_df = pd.concat([structured_data_df.reset_index(drop=True), ocr_df.reset_index(drop=True)], axis=1)
                else:
                    # If mismatch, just show OCR data for now or handle as per specific logic
                    print("Warning: Row count mismatch between ERP and OCR data. Showing OCR data primarily.")
                    integrated_df = ocr_df
            else:
                integrated_df = ocr_df
        elif structured_data_df is not None:
            integrated_df = structured_data_df
        else:
            integrated_df = pd.DataFrame()

        print("Data integration complete.")
        return integrated_df

if __name__ == '__main__':
    cleaner = DataCleaner()

    raw_text = "Invoice   Number: INV-001    Amount:  100.00   Supplier:  Test   Co.  "
    cleaned = cleaner.clean_ocr_text(raw_text)
    print(f"Cleaned Text: '{cleaned}'")

    supplier = "Test Co."
    std_supplier = cleaner.standardize_supplier_name(supplier)
    print(f"Standardized Supplier: '{std_supplier}'")

    summary = "Payment for services rendered"
    std_summary = cleaner.standardize_summary(summary)
    print(f"Standardized Summary: '{std_summary}'")

    # Example integration
    erp_example_data = pd.DataFrame({
        'voucher_id': ['V001', 'V002'],
        'erp_amount': [150.00, 200.00],
        'erp_date': ['2023-01-05', '2023-01-06']
    })

    ocr_example_data = [
        {'invoice_code': 'IC001', 'invoice_number': 'IN001', 'amount': 150.00, 'supplier_name': 'Supplier A Inc.'},
        {'invoice_code': 'IC002', 'invoice_number': 'IN002', 'amount': 200.00, 'supplier_name': 'Supplier B Ltd.'}
    ]

    integrated = cleaner.integrate_data(erp_example_data, ocr_example_data)
    print("\nIntegrated Data:")
    print(integrated)

    # Example with only OCR data
    ocr_only_data = [
        {'invoice_code': 'IC003', 'invoice_number': 'IN003', 'amount': 300.00, 'supplier_name': 'Supplier C Corp'}
    ]
    integrated_ocr_only = cleaner.integrate_data(None, ocr_only_data)
    print("\nIntegrated OCR Only Data:")
    print(integrated_ocr_only)