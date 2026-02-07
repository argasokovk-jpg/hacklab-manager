from fpdf import FPDF
import os
from datetime import datetime
from pathlib import Path

class SimplePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(29, 78, 216)
        self.cell(0, 10, 'HACKLAB MANAGER - PENTEST REPORT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f'Generated: {datetime.now().strftime("%d.%m.%Y %H:%M")}', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

class PDFGenerator:
    def __init__(self, username='hacker'):
        self.username = username
        self.reports_dir = Path.home() / '.hacklab' / 'reports'
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_lab_report(self, lab_id, analysis_data, sequence_data):
        pdf = SimplePDF()
        pdf.add_page()
        
        pdf.set_font('Arial', 'B', 20)
        pdf.set_text_color(29, 78, 216)
        pdf.cell(0, 20, 'PENETRATION TEST REPORT', 0, 1, 'C')
        
        pdf.set_font('Arial', 'B', 16)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f'LAB {lab_id}', 0, 1, 'C')
        pdf.ln(10)
        
        score = analysis_data.get('score', 0)
        level = analysis_data.get('level', 'Beginner')
        
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f'Score: {score}/100', 0, 1)
        pdf.cell(0, 10, f'Level: {level}', 0, 1)
        pdf.cell(0, 10, f'User: {self.username}', 0, 1)
        pdf.ln(10)
        
        tools_used = analysis_data.get('tools_used', [])
        if tools_used:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Tools Used:', 0, 1)
            pdf.set_font('Arial', '', 11)
            for tool in tools_used:
                pdf.cell(0, 8, f'  - {tool.replace("_", " ").title()}', 0, 1)
        
        pdf.ln(10)
        
        recommendations = analysis_data.get('recommendations', [])
        if recommendations:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Recommendations:', 0, 1)
            pdf.set_font('Arial', '', 11)
            for rec in recommendations[:5]:
                clean_rec = ''
                for char in str(rec):
                    if 32 <= ord(char) <= 126:
                        clean_rec += char
                    elif char in '[]+-':
                        clean_rec += char
                    else:
                        clean_rec += ' '
                pdf.cell(0, 8, f'  - {clean_rec}', 0, 1)
        
        if sequence_data:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Action Timeline:', 0, 1)
            pdf.set_font('Courier', '', 9)
            
            for i, action in enumerate(sequence_data[:20], 1):
                if len(action) >= 4:
                    timestamp = action[3]
                    tool = action[1]
                    target = action[2]
                    time_str = timestamp.split()[1] if ' ' in timestamp else timestamp
                    pdf.cell(0, 5, f'{i:2}. {time_str} | {tool:20} | {target[:40]}', 0, 1)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'lab_{lab_id}_{self.username}_{timestamp}.pdf'
        filepath = self.reports_dir / filename
        pdf.output(str(filepath))
        
        print(f'PDF report generated: {filepath}')
        return str(filepath)

if __name__ == "__main__":
    gen = PDFGenerator()
    test_data = {
        'score': 85,
        'level': 'Middle',
        'tools_used': ['network_info', 'port_check'],
        'recommendations': ['Test recommendation 1', 'Test recommendation 2']
    }
    gen.generate_lab_report(1, test_data, [])
