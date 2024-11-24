import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from domain.entities.user_data import UserData


class EmailSender:

    def send_email_with_results(self, user_data: UserData, results_path: str):
        smtp_server = os.getenv("MAIL_SERVER")
        smtp_sender = os.getenv("MAIL_SENDER")
        smtp_password = os.getenv("MAIL_SECRET")
        smtp_port = os.getenv("MAIL_ACCESS_PORT")

        msg = MIMEMultipart()
        msg["From"] = smtp_sender
        msg["To"] = user_data.get("user_email", False)
        msg["Subject"] = (
            "[🧬 FUNEXPRESSION]: Resultados da Análise de Expressão Diferencial"
        )

        body = f'Olá {user_data.get("user_name", "Usuário Funexpression")},\n Seguem informações referentes à análise da sua expressão diferencial\n'

        graphic_result = results_path.get("vulcano_graph")
        csv_result = results_path.get("csv_file")

        with open(graphic_result, "rb") as image_file:
            result_image = MIMEImage(image_file.read())
            msg.attach(result_image)

        with open(csv_result, "rb") as csv_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(csv_file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{csv_result}"',
            )
            msg.attach(part)

        # TODO: Adicionar srr dos arquivos de controle, experimento e o genoma de referência no e-mail
        # Padj e Log2FC , RunId

        body = f"""{body}
        Você solicitou uma análise de expressão diferencial de genes, segue em anexo seus resultados.
        Arquivos de entrada:
            Controle: 
            Experimento:
            Genoma:
        Parâmetros:
            Threshold Padj:
            Threshold Log2FC:
        Anexos:
            1. Gráfico volcano com os genes diferencialmente expressos classificados como UP/DOWN regulated
            2. Planilha com resultados detalhados de expressão diferencial de genes


        Esperamos que esta análise tenha sido divertida para você!
        [🍄 FUNEXPRESSION by G2BC]
        """

        msg.attach(MIMEText(body, "plain"))

        try:

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_sender, smtp_password)
            server.sendmail(
                smtp_sender, user_data.get("user_email", False), msg.as_string()
            )
            print("Email enviado com sucesso....")
            server.quit()

            return True
        except Exception as e:
            print(f"Erro ao enviar e-mail: {str(e)}")

            return False
