from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime

class QuotePDFGenerator:
    def __init__(self):
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(self.buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2e7d32')
        ))
    
    def generate_quote_pdf(self, quote_data):
        story = []
        
        title = Paragraph("ORÇAMENTO DE PAISAGISMO", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        quote_info = [
            ['Orçamento #:', str(quote_data.get('id', ''))],
            ['Cliente:', quote_data.get('client', '')],
            ['Data:', datetime.now().strftime('%d/%m/%Y')],
            ['Status:', quote_data.get('status', '')]
        ]
        
        info_table = Table(quote_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        items_data = [['Serviço', 'Qtd', 'Preço Unit.', 'Subtotal']]
        total = 0
        
        for item in quote_data.get('items', []):
            subtotal = float(item.get('quantity', 0)) * float(item.get('unit_price', 0))
            total += subtotal
            items_data.append([
                item.get('service_name', ''),
                str(item.get('quantity', '')),
                f"R$ {float(item.get('unit_price', 0)):.2f}",
                f"R$ {subtotal:.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e7d32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 20))
        
        total_data = [['TOTAL GERAL:', f"R$ {total:.2f}"]]
        total_table = Table(total_data, colWidths=[5*inch, 2*inch])
        total_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 2, colors.black)
        ]))
        
        story.append(total_table)
        
        self.doc.build(story)
        pdf_data = self.buffer.getvalue()
        self.buffer.close()
        
        return pdf_data