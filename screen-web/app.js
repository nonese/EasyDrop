const $ = (id) => document.getElementById(id);
const state = {
  server: "",
  deviceId: localStorage.getItem("device_id") || "",
  deviceSecret: localStorage.getItem("device_secret") || "",
  token: localStorage.getItem("device_token") || "",
  ws: null,
  manifestVersion: Number(localStorage.getItem("manifest_version") || "0"),
  playlist: [],
  index: 0,
};

function setStatus(text) {
  $("status").textContent = text;
}

function saveDevice() {
  localStorage.setItem("device_id", state.deviceId);
  localStorage.setItem("device_secret", state.deviceSecret);
  localStorage.setItem("device_token", state.token);
  localStorage.setItem("manifest_version", String(state.manifestVersion));
}

async function request(path, options = {}) {
  const headers = options.headers || {};
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const res = await fetch(`${state.server}${path}`, { ...options, headers });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function registerDevice() {
  state.server = $("server").value.trim();
  const name = $("name").value.trim();
  const data = await request("/api/devices/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, type: "web", meta: { ua: navigator.userAgent } }),
  });
  state.deviceId = data.device_id;
  state.deviceSecret = data.secret;
  saveDevice();
  setStatus(`registered: ${state.deviceId.slice(0, 8)}`);
}

async function loginDevice() {
  state.server = $("server").value.trim();
  if (!state.deviceId || !state.deviceSecret) throw new Error("请先注册设备");
  const data = await request("/api/devices/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ device_id: state.deviceId, secret: state.deviceSecret }),
  });
  state.token = data.device_token;
  saveDevice();
  setStatus("device logged in");
}

async function report(event, item) {
  try {
    await request("/api/logs/report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event, media_id: item?.media_id, ts: new Date().toISOString() }),
    });
  } catch (e) {
    console.warn("report failed", e);
  }
}

async function refreshManifest() {
  if (!state.deviceId) return;
  const data = await request(`/api/devices/${state.deviceId}/manifest?since_version=${state.manifestVersion}`);
  if (!data.changed) return;
  state.manifestVersion = data.version;
  state.playlist = data.playlist?.items || [];
  state.index = 0;
  saveDevice();
  setStatus(`manifest v${state.manifestVersion}, items=${state.playlist.length}`);
}

function renderCurrent() {
  const player = $("player");
  player.innerHTML = "";

  if (!state.playlist.length) {
    player.textContent = "暂无投放内容";
    return;
  }

  const item = state.playlist[state.index % state.playlist.length];
  if (item.type === "video") {
    const v = document.createElement("video");
    v.src = `${state.server}${item.url}`;
    v.autoplay = true;
    v.controls = false;
    v.muted = true;
    v.playsInline = true;
    v.onplay = () => report("play_start", item);
    v.onended = () => {
      report("play_end", item);
      state.index += 1;
      renderCurrent();
    };
    v.onerror = () => {
      report("error", item);
      state.index += 1;
      renderCurrent();
    };
    player.appendChild(v);
    v.play().catch(() => {});
    return;
  }

  const img = document.createElement("img");
  img.src = `${state.server}${item.url}`;
  img.onload = () => report("play_start", item);
  img.onerror = () => report("error", item);
  player.appendChild(img);
  setTimeout(() => {
    report("play_end", item);
    state.index += 1;
    renderCurrent();
  }, Math.max(1000, item.play_duration_ms || 5000));
}

function connectWs() {
  if (!state.token) return;
  const base = state.server.replace("http://", "ws://").replace("https://", "wss://");
  state.ws = new WebSocket(`${base}/ws/device?token=${encodeURIComponent(state.token)}`);

  state.ws.onopen = () => {
    setStatus("ws connected");
    state.ws.send(JSON.stringify({ type: "hello", device_id: state.deviceId, ts: new Date().toISOString() }));
    setInterval(() => {
      if (state.ws && state.ws.readyState === WebSocket.OPEN) {
        state.ws.send(JSON.stringify({ type: "heartbeat", device_id: state.deviceId, ts: new Date().toISOString() }));
      }
    }, 30000);
  };

  state.ws.onmessage = (ev) => {
    try {
      const msg = JSON.parse(ev.data);
      if (msg.type === "manifest_update") refreshManifest().then(renderCurrent);
    } catch (_) {}
  };

  state.ws.onclose = () => setStatus("ws closed");
}

async function startPlayback() {
  await refreshManifest();
  renderCurrent();
  connectWs();
  setInterval(async () => {
    await refreshManifest();
  }, 15000);
}

$("register").onclick = () => registerDevice().catch((e) => alert(e.message));
$("login").onclick = () => loginDevice().catch((e) => alert(e.message));
$("start").onclick = () => startPlayback().catch((e) => alert(e.message));

if (state.deviceId) setStatus(`device: ${state.deviceId.slice(0, 8)}`);
