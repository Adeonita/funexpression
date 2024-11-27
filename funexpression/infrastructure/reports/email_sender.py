import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from domain.entities.user_data import UserData


class EmailSender:

    def send_email_with_results(self, pipeline_info, results_path: str):

        smtp_server = os.getenv("MAIL_SERVER")
        smtp_sender = os.getenv("MAIL_SENDER")
        smtp_password = os.getenv("MAIL_SECRET")
        smtp_port = os.getenv("MAIL_ACCESS_PORT")

        run_id = pipeline_info.get("run_id")
        user_email = pipeline_info.get("user_email", False)
        user_name = pipeline_info.get("user_name", "Usuário Funexpression")
        control_organism = pipeline_info.get("control_organism")
        experiment_organism = pipeline_info.get("experiment_organism")

        control = (
            control_organism.get("srr_1")
            + ", "
            + control_organism.get("srr_2")
            + ", "
            + control_organism.get("srr_3")
        )
        experiment = (
            experiment_organism.get("srr_1")
            + ", "
            + experiment_organism.get("srr_2")
            + ", "
            + experiment_organism.get("srr_3")
        )

        reference_genome = pipeline_info.get("reference_genome")
        padj = pipeline_info.get("p_adj")
        log_2_fold_change_threshold = pipeline_info.get("log_2_fold_change_threshold")

        msg = MIMEMultipart()
        msg["From"] = smtp_sender
        msg["To"] = user_email
        msg["Subject"] = (
            "[🧬 FUNEXPRESSION]: Resultados da Análise de Expressão Diferencial"
        )

        body = f"Olá {user_name},\n Seguem informações referentes à análise da sua expressão diferencial\n"

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

        body = f"""{body}
        Você solicitou uma análise de expressão diferencial de genes, segue em anexo seus resultados.
        run_id: {run_id}
        Arquivos de entrada:
            Controle: {control}
            Experimento: {experiment}
            Genoma: {reference_genome}
        Parâmetros:
            Threshold Padj: {padj}
            Threshold Log2FC: ± {log_2_fold_change_threshold}
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
            server.sendmail(smtp_sender, user_email, msg.as_string())
            print("Email enviado com sucesso....")
            server.quit()

            return True
        except Exception as e:
            print(f"Erro ao enviar e-mail: {str(e)}")

            return False
