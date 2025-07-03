// script.js

$(document).ready(function() {
    // Referências aos elementos do DOM
    const chatMessages = $('#chat-messages');
    const userInput = $('#user-input');
    const sendButton = $('#send-button');
    const attachmentButton = $('#attachment-button'); 
    const voiceButton = $('#voice-button');
    const fileInput = $('#file-input');
    const chatOptionsMenu = $('.ui.labeled.icon.sidebar');
    const attachmentModal = $('#attachment-modal');
    const modelSelectorDropdown = $('#model-selector-dropdown'); // Nova referência ao dropdown de modelo

    // Referências aos botões dentro do modal de anexo
    const attachLocalButton = $('#attach-local-button');
    const attachOneDriveButton = $('#attach-onedrive-button');
    const attachGoogleDriveButton = $('#attach-google-drive-button');

    let selectedSector = null; // Armazena o setor selecionado pelo usuário
    let selectedModel = 'Gemini-Flash'; // Modelo de IA selecionado, padrão para Gemini-Flash
    let isRecording = false; // Estado de gravação de voz (simulado)

    // Inicialização da Sidebar do Semantic UI
    chatOptionsMenu.sidebar({
        context: $('body'),
        transition: 'overlay',
        dimPage: true,
        mobileTransition: 'overlay',
        exclusive: true
    }).sidebar('attach events', '#sidebar-toggle');

    // Inicialização do dropdown de seleção do modelo de IA
    modelSelectorDropdown.dropdown({
        onChange: function(value, text, $selectedItem) {
            selectedModel = value;
            addMessage(`Modelo de IA alterado para **${text}**.`, 'bot');
            // Aqui você poderia adicionar lógica para alternar a API LLM real, se suportado.
            // Por enquanto, apenas atualiza a interface.
        }
    });

    // Função para adicionar uma mensagem ao chat
    // Permite adicionar texto e, opcionalmente, uma imagem de preview
    function addMessage(text, sender, imageUrl = null) {
        const messageContainer = $('<div class="message-container ' + sender + '"></div>');
        let avatarSrc = '';
        let altText = '';

        // Define o avatar e texto alternativo com base no remetente
        if (sender === 'user') {
            avatarSrc = 'https://placehold.co/40x40/4285f4/ffffff?text=USER'; // Avatar do usuário
            altText = 'Avatar do Usuário';
        } else {
            avatarSrc = 'https://placehold.co/40x40/dddddd/000000?text=BOT'; // Avatar do bot
            altText = 'Avatar do Bot';
        }

        // Cria o elemento de imagem do avatar
        const avatar = $('<img src="' + avatarSrc + '" alt="' + altText + '" class="message-avatar">');
        // Cria a bolha de mensagem
        const messageBubble = $('<div class="ui message ' + sender + '"></div>');

        // Se houver uma URL de imagem, adiciona a imagem na bolha de mensagem
        if (imageUrl) {
            messageBubble.append('<img src="' + imageUrl + '" style="max-width: 100%; border-radius: 10px; margin-bottom: 10px;">');
        }
        // Adiciona o texto da mensagem
        messageBubble.append('<p>' + text + '</p>');

        // Anexa o avatar e a bolha de mensagem ao contêiner, na ordem correta
        if (sender === 'user') {
            messageContainer.append(messageBubble, avatar); // Avatar à direita para o usuário
        } else {
            messageContainer.append(avatar, messageBubble); // Avatar à esquerda para o bot
        }

        chatMessages.append(messageContainer); // Adiciona o contêiner de mensagem ao chat
        chatMessages.scrollTop(chatMessages[0].scrollHeight); // Rola para o final do chat
    }

    // Função para interagir com o backend Python para obter a resposta do LLM
    async function getLLMResponse(message, sector, fileData = null) {
        // Objeto de dados a ser enviado para o backend
        const requestData = {
            message: message,
            sector: sector,
            fileData: fileData // Inclui fileData se existir
        };

        try {
            // Faz uma requisição POST para o endpoint /chat da API FastAPI
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            // Verifica se a resposta da rede foi bem-sucedida
            if (!response.ok) {
                // Se a resposta não foi OK, lança um erro
                const errorText = await response.text();
                throw new Error(`Erro do servidor: ${response.status} ${response.statusText} - ${errorText}`);
            }

            const result = await response.json(); // Analisa a resposta JSON do backend
            return result.response; // Retorna a resposta do LLM
        } catch (error) {
            console.error('Erro ao comunicar com o backend:', error);
            return "Desculpe, houve um erro de comunicação com o servidor. Por favor, tente novamente mais tarde.";
        }
    }
    // Função para formatar o texto da resposta do LLM usando regex
    function formatLLMResponse(text) {
        // Headers (H1 a H6)
        text = text.replace(/^###### (.*$)/gim, '<h6>$1</h6>');
        text = text.replace(/^##### (.*$)/gim, '<h5>$1</h5>');
        text = text.replace(/^#### (.*$)/gim, '<h4>$1</h4>');
        text = text.replace(/^### (.*$)/gim, '<h3>$1</h3>');
        text = text.replace(/^## (.*$)/gim, '<h2>$1</h2>');
        text = text.replace(/^# (.*$)/gim, '<h1>$1</h1>');

        // Ênfase (Negrito **texto** e Itálico *texto*)
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Negrito
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>'); // Itálico

        // Destaques (mark ==texto==)
        text = text.replace(/==(.*?)==/g, '<mark>$1</mark>');

        // Código inline (`código`)
        text = text.replace(/`(.*?)`/g, '<code>$1</code>');

        // Blocos de código (```linguagem\ncódigo\n```)
        text = text.replace(/```(.*?)?\n([\s\S]*?)?\n```/g, '<pre><code>$2</code></pre>');

        // Citações em bloco (> Citação)
        text = text.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');
        
        // Listas (Bullet points - ou *)
        // Converte linhas de lista em <li> e envolve em <ul>
        let lines = text.split('\n');
        let inList = false;
        let formattedLines = [];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const trimmedLine = line.trim();
            if (trimmedLine.startsWith('- ') || trimmedLine.startsWith('* ')) {
                if (!inList) {
                    formattedLines.push('<ul>');
                    inList = true;
                }
                formattedLines.push('<li>' + trimmedLine.substring(2) + '</li>');
            } else {
                if (inList) {
                    formattedLines.push('</ul>');
                    inList = false;
                }
                formattedLines.push(line);
            }
        }
        if (inList) { // Fecha a lista se ela não foi fechada no final
            formattedLines.push('</ul>');
        }
        text = formattedLines.join('\n');


        // Quebras de linha para parágrafos
        text = text.replace(/\n/g, '<br>');

        return text;
    }
    // Evento de clique nos itens do menu da sidebar
    chatOptionsMenu.find('.item').on('click', async function() {
        // Verifica se é o item Dash Agro
        if ($(this).find('i').hasClass('leaf')) {
            return; // Deixa o onclick do HTML lidar com a navegação
        }
        
        selectedSector = $(this).data('sector'); // Obtém o setor do atributo data-sector
        chatOptionsMenu.sidebar('hide'); // Esconde a sidebar
        // Adiciona a mensagem do usuário confirmando a seleção do setor
        addMessage(`Você selecionou o setor **${$(this).text().trim()}**.`, 'user');

        // Define a mensagem inicial do bot com base no setor selecionado
        let initialBotMessage = '';
        switch (selectedSector) {
            case 'atendente':
                initialBotMessage = 'Ótimo! Em que posso ajudar você com o atendimento geral da Kognia?';
                break;
            case 'comercial':
                initialBotMessage = 'Excelente! Como posso te auxiliar em relação a orçamentos, produtos ou propostas da Kognia?';
                break;
            case 'tecnico':
                initialBotMessage = 'Certo! Por favor, descreva o problema ou a dúvida técnica que você tem com nossas soluções.';
                break;
        }
        addMessage(initialBotMessage, 'bot'); // Adiciona a mensagem do bot
        userInput.focus(); // Coloca o foco no campo de texto
    });

    // Evento de clique no botão de envio
    sendButton.on('click', async function() {
        const message = userInput.val().trim(); // Obtém o texto do textarea
        if (message) { // Verifica se a mensagem não está vazia
            addMessage(message, 'user'); // Adiciona a mensagem do usuário ao chat
            userInput.val(''); // Limpa o campo de texto

            addMessage('Digitando...', 'bot'); // Adiciona mensagem "Digitando..."
            const botTypingMessageContainer = chatMessages.children().last(); // Pega o contêiner da mensagem "Digitando..."

            // Chama a função para obter a resposta do LLM através do backend
            const botResponse = await getLLMResponse(message, selectedSector);

            botTypingMessageContainer.remove(); // Remove a mensagem "Digitando..."
            // Renderiza HTML na resposta do bot
            const messageContainer = $('<div class="message-container bot"></div>');
            const avatar = $('<img src="https://placehold.co/40x40/dddddd/000000?text=BOT" alt="Avatar do Bot" class="message-avatar">');
            const messageBubble = $('<div class="ui message bot"></div>');
            messageBubble.html(botResponse); // Usa .html() em vez de .text() para renderizar HTML
            messageContainer.append(avatar, messageBubble);
            chatMessages.append(messageContainer);
            chatMessages.scrollTop(chatMessages[0].scrollHeight);
        }
    });

    // Evento de clique no botão de anexo para abrir o modal
    attachmentButton.on('click', function() {
        attachmentModal.modal('show'); // Abre o modal
    });

    // Evento de clique para anexar do computador (aciona o input de arquivo)
    attachLocalButton.on('click', function() {
        attachmentModal.modal('hide'); // Esconde o modal
        fileInput.click(); // Dispara o clique no input de arquivo oculto
    });

    // Evento de clique para anexar do OneDrive (simulado)
    attachOneDriveButton.on('click', function() {
        attachmentModal.modal('hide'); // Esconde o modal
        addMessage('A funcionalidade de anexar do OneDrive é simulada e requer uma integração de API mais complexa com backend para funcionar. ', 'bot');
        addMessage('Simulando anexo de arquivo do OneDrive: "Documento_Simulado.docx" para análise. Por favor, digite sua mensagem. ', 'user');
        // Aqui você enviaria a "simulação" ao LLM através do backend
        getLLMResponse('O usuário está simulando o anexo de um arquivo do OneDrive chamado "Documento_Simulado.docx". ', selectedSector).then(response => {
            addMessage(response, 'bot');
        });
    });

    // Evento de clique para anexar do Google Drive (simulado)
    attachGoogleDriveButton.on('click', function() {
        attachmentModal.modal('hide'); // Esconde o modal
        addMessage('A funcionalidade de anexar do Google Drive é simulada e requer uma integração de API mais complexa com backend para funcionar. ', 'bot');
        addMessage('Simulando anexo de arquivo do Google Drive: "Planilha_Dados.xlsx" para análise. Por favor, digite sua mensagem. ', 'user');
        // Aqui você enviaria a "simulação" ao LLM através do backend
        getLLMResponse('O usuário está simulando o anexo de um arquivo do Google Drive chamado "Planilha_Dados.xlsx". ', selectedSector).then(response => {
            addMessage(response, 'bot');
        });
    });

    // Evento quando um arquivo é selecionado no input de arquivo (anexo local)
    fileInput.on('change', async function(e) {
        const file = e.target.files[0]; // Obtém o arquivo selecionado
        if (!file) return; // Se nenhum arquivo foi selecionado, sai da função

        // Verifica se o tipo de arquivo é suportado para análise (imagem ou texto simples)
        if (!file.type.startsWith('image/') && file.type !== 'text/plain') {
            addMessage('Desculpe, apenas imagens e arquivos de texto são suportados para análise. ', 'bot');
            e.target.value = null; // Limpa o input do arquivo para permitir re-upload
            return;
        }

        const reader = new FileReader(); // Cria um leitor de arquivos
        reader.onload = async function(event) {
            let fileData = {
                mimeType: file.type, // Tipo MIME do arquivo
                data: ''
            };
            let userMessageText = 'Anexou um arquivo. ';
            let filePreviewUrl = null;

            // Processa o arquivo com base no tipo
            if (file.type.startsWith('image/')) {
                fileData.data = event.target.result.split(',')[1]; // Pega apenas os dados base64
                userMessageText += `Uma imagem (${file.name}).`;
                filePreviewUrl = event.target.result; // URL para pré-visualização no chat
            } else if (file.type === 'text/plain') {
                userMessageText += `Um arquivo de texto (${event.target.result.substring(0, Math.min(event.target.result.length, 50))}...)`;
                fileData.data = btoa(event.target.result); // Codifica o texto para base64
            }

            addMessage(userMessageText, 'user', filePreviewUrl); // Adiciona a mensagem do usuário com preview
            userInput.val(''); // Limpa o campo de texto

            addMessage('Analisando anexo...', 'bot'); // Mensagem de processamento
            const botTypingMessageContainer = chatMessages.children().last();

            // Envia uma requisição ao LLM através do backend com a mensagem e os dados do arquivo
            const botResponse = await getLLMResponse("Analise o arquivo anexado e me diga o que você vê/entende ou resuma o conteúdo.", selectedSector, fileData);

            botTypingMessageContainer.remove(); // Remove a mensagem de processamento
            addMessage(botResponse, 'bot'); // Adiciona a resposta do bot
        };
        reader.readAsDataURL(file); // Lê o arquivo como Data URL (base64)
        e.target.value = null; // Limpa o input do arquivo
    });

    let mediaRecorder;
    let audioChunks = [];

    // Evento de clique no botão de voz
    voiceButton.on('click', async function() {
        if (!isRecording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
                
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    await processAudio(audioBlob);
                    stream.getTracks().forEach(track => track.stop());
                };
                
                mediaRecorder.start();
                isRecording = true;
                voiceButton.find('i').removeClass('microphone').addClass('red circle');
                addMessage('Gravando áudio... Clique novamente para parar.', 'bot');
            } catch (error) {
                addMessage('Erro ao acessar microfone. Verifique as permissões.', 'bot');
            }
        } else {
            mediaRecorder.stop();
            isRecording = false;
            voiceButton.find('i').removeClass('red circle').addClass('microphone');
        }
    });
    
    async function processAudio(audioBlob) {
        addMessage('Processando áudio...', 'bot');
        const botTypingMessageContainer = chatMessages.children().last();
        
        try {
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');
            formData.append('sector', selectedSector || '');
            
            const response = await fetch('http://localhost:8000/audio-chat', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Erro do servidor: ${response.status}`);
            }
            
            const result = await response.json();
            botTypingMessageContainer.remove();
            
            // Renderiza HTML na resposta do bot
            const messageContainer = $('<div class="message-container bot"></div>');
            const avatar = $('<img src="https://placehold.co/40x40/dddddd/000000?text=BOT" alt="Avatar do Bot" class="message-avatar">');
            const messageBubble = $('<div class="ui message bot"></div>');
            messageBubble.html(result.response);
            messageContainer.append(avatar, messageBubble);
            chatMessages.append(messageContainer);
            chatMessages.scrollTop(chatMessages[0].scrollHeight);
        } catch (error) {
            botTypingMessageContainer.remove();
            addMessage('Erro ao processar áudio. Tente novamente.', 'bot');
        }
    }

    // Evento de tecla 'Enter' no textarea (envia mensagem, Shift+Enter para nova linha)
    userInput.on('keypress', function(e) {
        if (e.which === 13 && !e.shiftKey) { // Se Enter for pressionado sem Shift
            e.preventDefault(); // Previne a quebra de linha padrão do textarea
            sendButton.click(); // Simula o clique no botão de envio
        }
    });

    // Ajuste automático da altura do textarea conforme o texto é digitado
    userInput.on('input', function() {
        this.style.height = 'auto'; // Reseta a altura para calcular o scrollHeight
        this.style.height = (this.scrollHeight) + 'px'; // Define a altura com base no conteúdo
    });

    // Aciona o evento 'input' uma vez ao carregar para definir a altura inicial correta
    userInput.trigger('input');
});
