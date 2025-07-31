// Usar API_URL global se já estiver definida
if (typeof API_URL === 'undefined') {
    var API_URL = "http://localhost:8000";
}

// Classe para geração de relatórios em PDF
class LandscapingReportGenerator {
    constructor() {
        this.apiUrl = API_URL;
    }

    // Gerar PDF do orçamento usando PDFKit
    async generateQuotePDF(quoteId) {
        try {
            // Buscar dados do orçamento
            const response = await fetch(`${this.apiUrl}/api/landscaping/quote/${quoteId}`, {
                headers: {
                    'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                }
            });

            if (!response.ok) {
                throw new Error('Erro ao buscar dados do orçamento');
            }
            
            const quote = await response.json();
            
            // Buscar itens do orçamento
            const itemsResponse = await fetch(`${this.apiUrl}/api/landscaping/quote/${quoteId}/items`, {
                headers: {
                    'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                }
            });
            
            if (itemsResponse.ok) {
                quote.items = await itemsResponse.json();
            }
            
            // Buscar dados do cliente
            const response_crm = await fetch(`${this.apiUrl}/api/landscaping/client/${quote["client_id"]}`, {
                headers: {
                    'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                }
            });
    
            const client = await response_crm.json();
            this.createQuotePDF(quote, client);
        } catch (error) {
            console.error('Erro ao gerar PDF:', error);
            alert('Erro ao gerar PDF do orçamento');
        }
    }

    // Criar PDF usando PDFKit
    createQuotePDF(quote, client) {
        const doc = new PDFDocument({ margin: 30, size: 'A4' });
        const chunks = [];
        
        doc.on('data', chunk => chunks.push(chunk));
        doc.on('end', () => {
            const pdfBlob = new Blob(chunks, { type: 'application/pdf' });
            const url = URL.createObjectURL(pdfBlob);
            window.open(url, '_blank');
        });
        
        // Fundo geral verde
        doc.rect(0, 0, 595, 842).fill("#32C036");
        
        // Cabeçalho
        this.addHeader(doc, quote, client); // <--- Passe o client aqui
        
        // Corpo branco
        doc.rect(30, 120, 535, 600).fill('#FFFFFF');
        
        // Tabela de itens
        this.addItemsTable(doc, quote);
        
        // Rodapé
        this.addFooter(doc);
        
        doc.end();
    }

    addHeader(doc, quote, client) {
        // Fundo do cabeçalho
        doc.rect(30, 30, 535, 80).fill("#FFEFCD");
        
        // Logotipo (imagem base64 ou URL)
        const logoBase64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==';
        
        try {
            doc.image(logoBase64, 40, 40, { width: 60, height: 40 });
        } catch (error) {
            // Se não conseguir carregar a imagem, desenha um retângulo como placeholder
            doc.rect(40, 40, 60, 40).stroke('#8CBB6B').fill('#8CBB6B');
            doc.fontSize(8).fillColor('black').text('LOGO', 65, 58);
        }
        
        // Título
        doc.fontSize(16)
           .fillColor('black')
           .text('Orçamento de Jardim', 120, 45);
        
        // Informações do cliente
        doc.fontSize(10)
           .text(`Cliente: ${client["client_name"]}`, 120, 70)
           .text(`Email: ${client["email"]}`, 420, 70)
           .text(`Endereço: ${client["address"]}`, 120, 85)
           .text(`Cidade:  ${client["city"]} - ${client["state"]}`, 280, 85)
           .text(`WhatsApp: ${this.formatPhoneNumber(client["phone_number"])}`, 420, 85);
    }

    addItemsTable(doc, quote) {
        let startY = 140;
        
        startY += 10;
        const itemHeight = 25;
        const tableWidth = 515; // Largura do fundo branco menos margens
        
        // Cabeçalho da tabela
        doc.rect(40, startY, tableWidth, itemHeight)
           .fill('#FFEFCD');
        
        doc.fontSize(11)
           .fillColor('black')
           .font('Helvetica-Bold')
           .text('Descrição', 50, startY + 8)
           .text('Qtde.', 260, startY + 8)
           .text('Preço unitário', 360, startY + 8)
           .text('Total', 470, startY + 8);
        
        let currentY = startY + itemHeight;
        let total = 0;
        
        // Itens da tabela
        if (quote.items && quote.items.length > 0) {
            quote.items.forEach(item => {
                const subtotal = item.quantity * item.unit_price;
                total += subtotal;
                
                // Usar descrição do item se disponível, senão usar service_name
                const itemDescription = item.description || item.service_name || 'Serviço';
                
                doc.fontSize(10)
                   .fillColor('black')
                   .font('Helvetica')
                   .text(itemDescription, 50, currentY + 8)
                   .text(item.quantity.toString(), 260, currentY + 8)
                   .text(this.formatCurrency(item.unit_price), 360, currentY + 8)
                   .text(this.formatCurrency(subtotal), 470, currentY + 8);
                
                currentY += itemHeight;
            });
        }
        
        // Total Geral
        doc.rect(40, currentY, tableWidth, itemHeight)
           .fill("#8CBB6B");
        
        doc.fontSize(12)
           .fillColor('black')
           .font('Helvetica-Bold')
           .text('Total do Orçamento:', 320, currentY + 8)
           .text(this.formatCurrency(total), 470, currentY + 8);
    }

    addFooter(doc) {
        // Rodapé com informações da empresa
        const footerY = 750;
        
        doc.fontSize(10)
           .fillColor('white')
           .text('KOGNIA PAISAGISMO', 50, footerY, { align: 'center', width: 495 })
           .text('Endereço: Rua das Flores, 123 - São Paulo - SP', 50, footerY + 15, { align: 'center', width: 495 })
           .text('Site: www.kogniapaisagismo.com.br | Email: contato@kogniapaisagismo.com.br', 50, footerY + 30, { align: 'center', width: 495 })
           .text('Telefone: (11) 3333-4444 | WhatsApp: (11) 99999-8888', 50, footerY + 45, { align: 'center', width: 495 });
    }

    formatDate(dateString) {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleDateString('pt-BR');
    }

    formatPhoneNumber(phone) {
        if (!phone) return '-';
        const cleaned = phone.replace(/\D/g, '');
        if (cleaned.length === 11) {
            return `(${cleaned.slice(0, 2)}) ${cleaned.slice(2, 7)}-${cleaned.slice(7)}`;
        }
        return phone;
    }

    formatCurrency(value) {
        if (!value) return 'R$ 0,00';
        return parseFloat(value).toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
    }

    // Gerar PDF de projeto (futuro)
    generateProjectPDF(projectId) {
        window.open(`${this.apiUrl}/api/landscaping/project/${projectId}/pdf?user_id=1`, '_blank');
    }

    // Gerar PDF de relatório de manutenção (futuro)
    generateMaintenancePDF(maintenanceId) {
        window.open(`${this.apiUrl}/api/landscaping/maintenance/${maintenanceId}/pdf?user_id=1`, '_blank');
    }

    // Gerar PDF de relatório de cliente (futuro)
    generateClientPDF(clientId) {
        window.open(`${this.apiUrl}/api/landscaping/client/${clientId}/pdf?user_id=1`, '_blank');
    }
}

// Instância global do gerador de relatórios
const reportGenerator = new LandscapingReportGenerator();

// Função global para compatibilidade com código existente
function generateQuotePDF(id) {
    reportGenerator.generateQuotePDF(id);
}

// Funções globais para futuros relatórios
function generateProjectPDF(id) {
    reportGenerator.generateProjectPDF(id);
}

function generateMaintenancePDF(id) {
    reportGenerator.generateMaintenancePDF(id);
}

function generateClientPDF(id) {
    reportGenerator.generateClientPDF(id);
}