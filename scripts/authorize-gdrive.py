#!/usr/bin/env python3
"""
Autorizzazione OAuth per Google Drive (eseguire UNA SOLA VOLTA).
Crea credentials-gdrive.json con le credenziali autorizzate.
"""

import sys
import json
from google.auth.oauthlib.flow import InstalledAppFlow
from pathlib import Path


SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def main():
    if len(sys.argv) < 2:
        print("Uso: python authorize-gdrive.py <path-al-json-scaricato-da-google>")
        print("\nEsempio: python authorize-gdrive.py ~/Downloads/client_secret_xxxxx.json")
        sys.exit(1)

    client_secret_file = sys.argv[1]

    if not Path(client_secret_file).exists():
        print(f"Errore: file non trovato: {client_secret_file}")
        sys.exit(1)

    print("Avvio autorizzazione OAuth per Google Drive...")
    print("Si aprirà il browser per autenticazione.")

    try:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
        creds = flow.run_local_server(port=0)

        credentials_dict = {
            "type": "authorized_user",
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "refresh_token": creds.refresh_token,
        }

        output_file = Path(__file__).parent / "credentials-gdrive.json"
        with open(output_file, "w") as f:
            json.dump(credentials_dict, f, indent=2)

        print(f"\n✓ Autorizzazione completata!")
        print(f"✓ Credenziali salvate in: {output_file}")
        print("\nIl file download-report-from-gdrive.py ora funzionerà automaticamente.")

    except Exception as e:
        print(f"\n✗ Errore: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
