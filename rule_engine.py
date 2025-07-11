# review_engine/rule_engine.py
import pandas as pd

class RuleEngine:
    def __init__(self):
        self.rules = []
        self._load_default_rules()

    def _load_default_rules(self):
        """Loads a predefined set of rules for audit report review."""
        # 1. 数据一致性规则 (刚性校验)
        self.add_rule(
            name="Revenue Data Consistency Check (within 1%)",
            condition=lambda data: abs(data.get('reported_revenue', 0) - data.get('ledger_revenue', 0)) / (data.get('ledger_revenue', 1) + 1e-9) < 0.01,
            description="检查报告中披露的营业收入与账面数据差异是否小于1%。",
            severity="High"
        )
        self.add_rule(
            name="Audit Adjustment Disclosure Check",
            condition=lambda data: data.get('audit_adjustments_disclosed', False) == True if data.get('has_audit_adjustments', False) else True,
            description="检查若存在审计调整事项，是否在报表附注中详细披露。",
            severity="High"
        )

        # 3. 合规性与行业标准规则
        self.add_rule(
            name="Audit Procedure Completeness Check",
            condition=lambda data: all(proc in data.get('audit_procedures_described', []) for proc in ['函证', '监盘']) if data.get('is_financial_audit', False) else True,
            description="检查金融行业审计报告是否提及了必要的审计程序（函证、监盘）。",
            severity="Medium"
        )
        self.add_rule(
            name="Key Audit Matters Analysis Check",
            condition=lambda data: '为何对审计重要' in data.get('kam_description', '') if data.get('has_kam', False) else True,
            description="检查关键审计事项段落是否包含‘为何对审计重要’的分析。",
            severity="Medium"
        )
        # Add more rules here based on user's requirements

    # Helper functions for rules can be added here if needed, similar to _is_valid_date_sequence

    def add_rule(self, name, condition, description, severity):
        """Adds a new rule to the engine.
        Args:
            name (str): Name of the rule.
            condition (callable): A function that takes a data dictionary (representing a voucher)
                                  and returns True if the condition is met (passes), False otherwise.
            description (str): Description of what the rule checks.
            severity (str): Severity of the rule if violated (e.g., High, Medium, Low).
        """
        self.rules.append({
            'name': name,
            'condition': condition,
            'description': description,
            'severity': severity
        })
        print(f"Rule '{name}' added.")

    def apply_rules(self, voucher_data):
        """Applies all loaded rules to a single voucher.
        Args:
            voucher_data (dict): A dictionary containing the data for one voucher.
        Returns:
            list: A list of rule violation dictionaries. Each dict contains:
                  {'rule_name', 'description', 'severity', 'data_point' (optional)}
                  Returns an empty list if no rules are violated.
        """
        violations = []
        print(f"\nApplying rules to report: {voucher_data.get('report_id', 'N/A')}")
        for rule in self.rules:
            try:
                if not rule['condition'](voucher_data):
                    violations.append({
                        'rule_name': rule['name'],
                        'description': rule['description'],
                        'severity': rule['severity'],
                        'details': f"Failed on report {voucher_data.get('report_id', 'N/A')}"
                    })
                    print(f"Violation: {rule['name']} for report {voucher_data.get('report_id', 'N/A')}")
            except Exception as e:
                print(f"Error applying rule '{rule['name']}' to report {voucher_data.get('report_id', 'N/A')}: {e}")
                violations.append({
                    'rule_name': rule['name'],
                    'description': f"Error during rule execution: {e}",
                    'severity': 'Critical',
                    'details': f"Error on report {voucher_data.get('report_id', 'N/A')}"
                })
        return violations

    def apply_rules_to_batch(self, vouchers_df):
        """Applies rules to a DataFrame of vouchers.
        Args:
            vouchers_df (pd.DataFrame): DataFrame where each row is a voucher.
        Returns:
            pd.DataFrame: DataFrame with an additional 'rule_violations' column containing
                          a list of violation dicts for each voucher.
        """
        if not isinstance(vouchers_df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        print(f"\nApplying rules to batch of {len(vouchers_df)} vouchers...")
        results = []
        for index, row in vouchers_df.iterrows():
            voucher_dict = row.to_dict()
            violations = self.apply_rules(voucher_dict)
            results.append(violations)
        
        # It's often better to return a new DataFrame or add as a new column
        # For simplicity, we can add it as a new column to the input DataFrame
        vouchers_df_copy = vouchers_df.copy()
        vouchers_df_copy['rule_violations'] = results
        print("Batch rule application complete.")
        return vouchers_df_copy

if __name__ == '__main__':
    engine = RuleEngine()

    # Example audit report data
    report_compliant = {
        'report_id': 'AR202501',
        'reported_revenue': 1000000.00,
        'ledger_revenue': 1005000.00, # Within 1% difference
        'has_audit_adjustments': False,
        'audit_adjustments_disclosed': False,
        'is_financial_audit': True,
        'audit_procedures_described': ['函证', '监盘', '分析性复核'],
        'has_kam': True,
        'kam_description': '该事项为何对审计重要：存货跌价准备对财务报表影响重大。'
    }

    report_revenue_mismatch = {
        'report_id': 'AR202502',
        'reported_revenue': 900000.00,
        'ledger_revenue': 1000000.00, # >1% difference
        'has_audit_adjustments': False,
        'audit_adjustments_disclosed': False,
        'is_financial_audit': True,
        'audit_procedures_described': ['函证', '监盘'],
        'has_kam': True,
        'kam_description': '该事项为何对审计重要：收入确认政策复杂。'
    }

    report_missing_disclosure = {
        'report_id': 'AR202503',
        'reported_revenue': 500000.00,
        'ledger_revenue': 500000.00,
        'has_audit_adjustments': True,
        'audit_adjustments_disclosed': False, # Missing disclosure
        'is_financial_audit': True,
        'audit_procedures_described': ['函证', '监盘'],
        'has_kam': True,
        'kam_description': '该事项为何对审计重要：关联方交易复杂。'
    }

    report_missing_procedure = {
        'report_id': 'AR202504',
        'reported_revenue': 200000.00,
        'ledger_revenue': 200000.00,
        'has_audit_adjustments': False,
        'audit_adjustments_disclosed': False,
        'is_financial_audit': True,
        'audit_procedures_described': ['分析性复核'], # Missing '函证', '监盘'
        'has_kam': True,
        'kam_description': '该事项为何对审计重要：应收账款回收风险。'
    }

    report_kam_no_analysis = {
        'report_id': 'AR202505',
        'reported_revenue': 300000.00,
        'ledger_revenue': 300000.00,
        'has_audit_adjustments': False,
        'audit_adjustments_disclosed': False,
        'is_financial_audit': True,
        'audit_procedures_described': ['函证', '监盘'],
        'has_kam': True,
        'kam_description': '存货跌价准备。' # Missing "为何对审计重要"
    }

    print("--- Testing Single Reports ---")
    violations_compliant = engine.apply_rules(report_compliant)
    print(f"Violations for AR202501 (should be none): {violations_compliant}")

    violations_revenue = engine.apply_rules(report_revenue_mismatch)
    print(f"Violations for AR202502 (revenue mismatch): {violations_revenue}")

    violations_disclosure = engine.apply_rules(report_missing_disclosure)
    print(f"Violations for AR202503 (missing disclosure): {violations_disclosure}")

    violations_procedure = engine.apply_rules(report_missing_procedure)
    print(f"Violations for AR202504 (missing procedure): {violations_procedure}")

    violations_kam = engine.apply_rules(report_kam_no_analysis)
    print(f"Violations for AR202505 (KAM no analysis): {violations_kam}")

    print("\n--- Testing Batch Reports ---")
    reports_list = [
        report_compliant,
        report_revenue_mismatch,
        report_missing_disclosure,
        report_missing_procedure,
        report_kam_no_analysis
    ]

    reports_df = pd.DataFrame(reports_list)
    reviewed_reports_df = engine.apply_rules_to_batch(reports_df)
    print("\n--- Batch Review Results (DataFrame) ---")
    print(reviewed_reports_df[['report_id', 'rule_violations']])