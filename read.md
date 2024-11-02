### README para o Projeto Ignitor RF

# Ignitor RF

Este projeto implementa uma aplicação GUI para controlar um dispositivo Ignitor RF via comunicação serial. A aplicação é desenvolvida em Python utilizando a biblioteca [`customtkinter`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A6%2C%22character%22%3A7%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition") para a interface gráfica e a biblioteca `pyserial` para a comunicação serial.

## Funcionalidades

### Interface Gráfica (GUI)

A interface gráfica é construída utilizando [`customtkinter`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A6%2C%22character%22%3A7%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition") e possui as seguintes funcionalidades:

- **Conectar**: Conecta ao dispositivo Ignitor RF via porta serial.
- **Iniciar Contagem**: Inicia um processo de contagem regressiva antes de ativar o dispositivo.
- **Fechar**: Fecha a aplicação.
- **Salvar Log**: Salva o log de mensagens recebidas do dispositivo.
- **Parar Log**: Para o processo de logging (inicialmente oculto).
- **Tare**: Envia um comando de tara ao dispositivo (inicialmente oculto).

### Comunicação Serial

A aplicação se comunica com o dispositivo Ignitor RF via porta serial. As principais funcionalidades de comunicação incluem:

- **Conectar**: Estabelece uma conexão serial com o dispositivo.
- **Desconectar**: Fecha a conexão serial.
- **Receber Dados**: Lê continuamente dados da porta serial e atualiza a interface com as mensagens recebidas.
- **Enviar Comandos**: Envia comandos específicos ao dispositivo via porta serial (ativar, desativar, salvar log, parar log, tara).

### Processos

- **Contagem Regressiva**: Inicia uma contagem regressiva antes de enviar o comando de ativação ao dispositivo.
- **Logging**: Salva as mensagens recebidas do dispositivo em um arquivo de log.

## Estrutura do Código

### Classe Principal: [`IgnitorRFApp`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A10%2C%22character%22%3A6%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")

A classe [`IgnitorRFApp`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A10%2C%22character%22%3A6%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition") herda de [`Ctk.CTk`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A6%2C%22character%22%3A24%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition") e configura a interface gráfica e a comunicação serial.

#### Métodos Principais

- **[`__init__`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A11%2C%22character%22%3A8%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Inicializa a aplicação, configura a interface e atualiza as portas disponíveis.
- **[`configure_grid`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A15%2C%22character%22%3A13%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Configura o layout de grade da janela principal.
- **[`configure_buttons`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A17%2C%22character%22%3A13%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Configura os botões da interface.
- **[`configure_labels`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A18%2C%22character%22%3A13%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Configura os labels da interface.
- **[`update_ports`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A16%2C%22character%22%3A13%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Atualiza a lista de portas seriais disponíveis.
- **[`connect`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A31%2C%22character%22%3A55%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Conecta ao dispositivo via porta serial.
- **[`disconnect`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A86%2C%22character%22%3A49%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Desconecta do dispositivo.
- **[`quit`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A41%2C%22character%22%3A53%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Fecha a aplicação.
- **[`start_countdown`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A36%2C%22character%22%3A63%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Inicia o processo de contagem regressiva.
- **[`cancel`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A112%2C%22character%22%3A68%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Cancela o processo de contagem regressiva.
- **[`save_log`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A45%2C%22character%22%3A57%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Salva o log de mensagens recebidas.
- **[`stop_log`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A50%2C%22character%22%3A56%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Para o processo de logging.
- **[`send_tare`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A56%2C%22character%22%3A51%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Envia o comando de tara ao dispositivo.

### Funções Auxiliares

- **[`get_date_time`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A144%2C%22character%22%3A4%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Retorna a data e hora atual como uma string formatada.
- **[`connect`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A31%2C%22character%22%3A55%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Estabelece uma conexão serial com o dispositivo.
- **[`disconnect`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A86%2C%22character%22%3A49%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Fecha a conexão serial.
- **[`recebido`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A151%2C%22character%22%3A28%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Lê continuamente dados da porta serial.
- **[`send_command`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A180%2C%22character%22%3A4%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Envia um comando específico ao dispositivo.
- **[`fire`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A194%2C%22character%22%3A4%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Envia o comando de ativação ao dispositivo.
- **[`deactivate`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A198%2C%22character%22%3A4%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Envia o comando de desativação ao dispositivo.
- **[`count_down`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A111%2C%22character%22%3A23%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Processo de contagem regressiva antes de ativar o dispositivo.
- **[`esp_save_log`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A206%2C%22character%22%3A8%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Envia o comando para salvar o log no dispositivo.
- **[`esp_stop_log`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A135%2C%22character%22%3A12%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Envia o comando para parar o logging no dispositivo.
- **[`esp_tare`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A141%2C%22character%22%3A12%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Envia o comando de tara ao dispositivo.
- **[`save_serial_log`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A130%2C%22character%22%3A8%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Salva o log de mensagens em um arquivo.
- **[`get_com_ports`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A249%2C%22character%22%3A4%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Retorna uma lista de portas COM disponíveis.
- **[`get_usb_ports`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A253%2C%22character%22%3A4%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Retorna uma lista de portas USB disponíveis.
- **[`check_usb_connection`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A74%2C%22character%22%3A16%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Verifica as conexões USB disponíveis no sistema.
- **[`check_still_connect`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A161%2C%22character%22%3A10%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition")**: Verifica se a porta serial ainda está conectada.

## Requisitos

- Python 3.x
- Bibliotecas: [`customtkinter`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fviniciusmonnerat%2FDocumentos%2FSerra_Rocketry%2FIgnitorRF%2Fasync_ign.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A6%2C%22character%22%3A7%7D%7D%5D%2C%222f101d3b-85ce-4b46-976b-f10cf02ae4cd%22%5D "Go to definition"), `pyserial`

## Instalação

1. Clone o repositório:

   ```sh
   git clone https://github.com/seu-usuario/ignitor-rf.git
   cd ignitor-rf
   ```

2. Instale as dependências:
   ```sh
   pip install customtkinter pyserial
   ```

## Uso

1. Conecte o dispositivo Ignitor RF ao seu computador via USB.
2. Execute a aplicação:
   ```sh
   python async_ign.py
   ```
3. Na interface gráfica, selecione a porta serial correspondente ao dispositivo e clique em "Conectar".
4. Utilize os botões para iniciar a contagem regressiva, salvar logs, enviar comandos de tara, etc.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
