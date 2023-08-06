# We import necessary libraries 
from getpass import getpass
import smtplib
from email.message import EmailMessage
import numpy as np
import pandas as pd

# This class handles the process of sending emails
class EmailHandler():
    """A class to handle email operations including sending emails and reading email content from a file."""
    def __init__(self, email_username, email_domain="smtp.gmail.com", port=587, password=None, verbose=False):
        """
        Initializes the EmailHandler class.

        Args:
            email_username (str): The username of the email.
            email_domain (str, optional): The email domain. Defaults to 'smtp.gmail.com'.
            port (int, optional): The port to use for SMTP. Defaults to 587.
            password (str, optional): The password of the email. If None, prompts for input. Defaults to None.
            verbose (bool, optional): If True, prints login attempts. Defaults to False.

        Raises:
            SMTPAuthenticationError: If email login fails.
        """

        if password is None:
            self.password = getpass()  # Get the password securely if not provided
        else:
            self.password = password
        self.username = email_username
        self.domain = email_domain
        self.verbose = verbose
        self.port = port
        if self.verbose:
            print("Trying login...")
        # Create an SMTP server instance and log in
        with smtplib.SMTP(self.domain, self.port) as server:
            server.starttls()  # Upgrade the connection to a secure one using TLS
            server.login(self.username, self.password)
        if self.verbose:
            print("... success!")

    # Function to write and send an email
    def write_email(self, email_address, subject, content, from_address=None):
        """
        Writes and sends an email.

        Args:
            email_address (str): The recipient email address.
            subject (str): The subject of the email.
            content (str): The content of the email.
            from_address (str, optional): The sender's email address. If None, the initialized username is used. Defaults to None.

        Returns:
            int: 0 if the email is sent successfully.

        Raises:
            SMTPRecipientsRefused: If recipient’s mail server did not accept the email.
            SMTPHeloError: If the server didn’t reply properly to the HELO greeting.
            SMTPSenderRefused: If the server didn’t accept the from_addr.
            SMTPDataError: If the server replied with an unexpected error code.
        """        
        msg = EmailMessage()
        msg.set_content(content)

        if from_address is None:
            msg['From'] = self.username + "@" + self.domain
        else:
            msg['From'] = from_address
        msg['To'] = email_address
        msg['Subject'] = subject
        # Send the email
        with smtplib.SMTP(self.domain, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
        return 0
    

    def read_content_from_textfile(self, textfile, sender_name, recipient_name):
        """
        Reads a text file and replaces placeholders with sender and recipient names.

        Args:
            textfile (str): The path to the text file.
            sender_name (str): The name of the sender.
            recipient_name (str): The name of the recipient.

        Returns:
            str: The content of the text file with placeholders replaced.

        Raises:
            FileNotFoundError: If the provided textfile path does not exist.
        """

        with open(textfile) as fp:
            # Read the file and replace placeholder names
            content = fp.read().replace("YOURNAME", sender_name).replace("RECIPIENTNAME", recipient_name)
        return content


def send_emails(df,email_username, email_smtp_domain, email_password=None, email_smtp_port=587,
                dry_run=False):
    """
    Function that sends emails to the participants of a ride share program based on groups created.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing participant information, including names, email addresses, and groups.
        Required columns are ["Name", "Email", "arrival_group", "departure_group", 
        "date_time_of_airport_arrival", "date_time_of_hotel_departure"].
    email_username : str
        The username of the email to be used to send emails.
    email_smtp_domain : str
        The SMTP domain for the email to be used.
    email_password : str, optional
        The password of the email to be used to send emails. If None, user will be prompted for password. Default is None.
    email_smtp_port : int, optional
        The SMTP port to be used for the email server. Default is 587.

    Raises
    ------
    AssertionError
        If 'arrival_group' and 'departure_group' columns are not found in the DataFrame.
    """
    
    eh = EmailHandler(email_username, email_domain = email_smtp_domain, 
                      port = email_smtp_port, password = email_password, verbose=True)
    # df = pd.read_csv("optimized_clustering.csv")
    if not ("arrival_group" in df.columns and "departure_group" in df.columns):
        raise AssertionError("Error: arrival_group and departure_group columns not found in dataframe! \n"\
                             +"Please run the optimize routine first")

    helperstr = {}
    helperstr["arrival"] = """based on your planned arrival times, we suggest that you share a ride from the airport to your hotel.
You have said that you want to leave the airport at the following times"""
    helperstr["departure"] = """based on your planned departure times, we suggest that you share a ride from your hotel to the airport.
You have said that you want to leave the hotel at the following times"""
    colnames = {}
    colnames["arrival"] = "date_time_of_airport_arrival"
    colnames["departure"] = "date_time_of_hotel_departure"
    for kind in ["arrival", "departure"]:
        groups = np.unique(df[f"{kind}_group"])
        for group in groups:
            mask = (df[f"{kind}_group"] == group)
            names = df["Name"][mask].values
            first_names = []
            for name in names:
                first_names.append(name.split(" ")[0]) #only address by first names
            arrival_times = df[colnames[kind]][mask].values
            emails = list(df["Email"][mask].values)
            phone_numbers = list(df["Phone_number"][mask].values)
        
            address = ""
            for name in first_names:
                address += name+", "
            
            deptimes = ""
            for x in range(len(first_names)):
                deptimes += "\t"+names[x]+": "+pd.to_datetime(arrival_times[x]).strftime("%b %d, %I:%M %p")
                # if not phone_numbers[x]=="NaN":
                #     deptimes +=", contact number: "+phone_numbers[x]
                # TODO: to implement in later release
                deptimes +="\n "
            message = f"""
Dear {address}

{helperstr[kind]}:\n{deptimes}
Please contact each other and organize a ride together. If you have any questions, please contact us.

Best regards,
    The code/astro Team
            """
            print("Writing to: ",emails)
            # print(message)
        
    # Compose arrival message
            if np.sum(mask) < 2:
                if(kind == "arrival"):
                    content=f"""Dear {first_names[0]},
We are writing to you because you have indicated that you would like to share a ride from the airport to your hotel.
Unfortunately, we have not been able to find any other participants who arrive at the same time.
If you would like to share a ride, please contact us and we will try to find a solution.

Best regards,
    The code/astro Team"""
                else:
                    content=f"""Dear {first_names[0]},
We are writing to you because you have indicated that you would like to share a ride from your hotel to the airport.
Unfortunately, we have not been able to find any other participants who depart at the same time.
If you would like to share a ride, please contact us and we will try to find a solution.

Best regards,
    The code/astro Team"""
                if dry_run:
                    print("Email subject: ",f"[code/astro] Rideshare for your {kind}")
                    print("Email content: ",content)
                else:
                    eh.write_email(emails, subject=f"[code/astro] Rideshare for your {kind}", 
                                content = content)
            else: # more than 2 people in the group
                if(dry_run):
                    print("Email subject: ",f"[code/astro] Rideshare for your {kind}")
                    print("Email content: ",message)
                else:
                    eh.write_email(emails, subject=f"[code/astro] Rideshare for your {kind}", 
                                content=message)
