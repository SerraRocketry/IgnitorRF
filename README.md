# Ignitor RF

Este projeto implementa uma aplicação GUI para controlar um dispositivo Ignitor RF via comunicação serial. A aplicação é desenvolvida em Python utilizando a biblioteca `customtkinter` para a interface gráfica e a biblioteca `pyserial` para a comunicação serial.

## Funcionalidades

### Interface Gráfica (GUI)

A interface gráfica é construída utilizando `customtkinter` e possui as seguintes funcionalidades:

- **Conectar**: Conecta a um dispositivo via porta serial.
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

### Classe Principal: `IgnitorRFApp`

A classe `IgnitorRFApp` configura a interface gráfica e a comunicação serial.

#### Métodos Principais

- **[`__init__`]**: Inicializa a aplicação, configura a interface e atualiza as portas disponíveis.
- **[`configure_grid`]**: Configura o layout de grade da janela principal.
- **[`configure_buttons`]**: Configura os botões da interface.
- **[`configure_labels`]**: Configura os labels da interface.
- **[`update_ports`]**: Atualiza a lista de portas seriais disponíveis.
- **[`connect`]**: Conecta ao dispositivo via porta serial.
- **[`disconnect`]**: Desconecta do dispositivo.
- **[`quit`]**: Fecha a aplicação.
- **[`start_countdown`]**: Inicia o processo de contagem regressiva.
- **[`cancel`]**: Cancela o processo de contagem regressiva.
- **[`save_log`]**: Salva o log de mensagens recebidas.
- **[`stop_log`]**: Para o processo de logging.
- **[`send_tare`]**: Envia o comando de tara ao dispositivo.

### Funções Auxiliares

- **[`get_date_time`]**: Retorna a data e hora atual como uma string formatada.
- **[`connect`]**: Estabelece uma conexão serial com o dispositivo.
- **[`disconnect`]**: Fecha a conexão serial.
- **[`recebido`]**: Lê continuamente dados da porta serial.
- **[`send_command`]**: Envia um comando específico ao dispositivo.
- **[`fire`]**: Envia o comando de ativação ao dispositivo.
- **[`deactivate`]**: Envia o comando de desativação ao dispositivo.
- **[`count_down`]**: Processo de contagem regressiva antes de ativar o dispositivo.
- **[`esp_save_log`]**: Envia o comando para salvar o log no dispositivo.
- **[`esp_stop_log`]**: Envia o comando para parar o logging no dispositivo.
- **[`esp_tare`]**: Envia o comando de tara ao dispositivo.
- **[`save_serial_log`]**: Salva o log de mensagens em um arquivo.
- **[`get_com_ports`]**: Retorna uma lista de portas COM disponíveis.
- **[`get_usb_ports`]**: Retorna uma lista de portas USB disponíveis.
- **[`check_usb_connection`]**: Verifica as conexões USB disponíveis no sistema.
- **[`check_still_connect`]**: Verifica se a porta serial ainda está conectada.

## Requisitos

- Python 3.7+
- Bibliotecas:
  - `customtkinter`
  - `pyserial`

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/ViniciusCMB/IgnitorRF.git
cd IgnitorRF
pip install -r requirements.txt
```

## Uso

1. Conecte um dispositivo serial ao seu computador via USB.
2. Execute a aplicação:
   ```sh
   python async_ign.py
   ```
   - Execute o script `async_ign.py` para iniciar o controle dos ignitores usando uma interface gráfica, ou execute o script `async_cmd.py` para iniciar o controle dos ignitores usando linha de comando:
3. Na interface gráfica, selecione a porta serial correspondente ao dispositivo e clique em "Conectar".
4. Utilize os botões para iniciar a contagem regressiva, salvar logs, enviar comandos de tara, etc.

## Estrutura do Projeto

- `async_ign.py`: Script para controle assíncrono dos ignitores via RF usando user interface.
- `async_cmd.py`: Script para controle assíncrono dos ignitores via RF usando command line.
- `README.md`: Documentação do projeto.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.
