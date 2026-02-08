const $ = (id) => document.getElementById(id);
const SERVER_KEY = "backend_url";
const PANEL_COLLAPSED_KEY = "panel_collapsed";
const DEFAULT_SERVER = "http://127.0.0.1:8000";

const state = {
  server: localStorage.getItem(SERVER_KEY) || DEFAULT_SERVER,
  deviceId: localStorage.getItem("device_id") || "",
  deviceSecret: localStorage.getItem("device_secret") || "",
  token: localStorage.getItem("device_token") || "",
  ws: null,
  heartbeatTimer: null,
  pollTimer: null,
  started: false,
  manifestVersion: Number(localStorage.getItem("manifest_version") || "0"),
  playlist: [],
  index: 0,
  panelCollapsed: localStorage.getItem(PANEL_COLLAPSED_KEY) === "1",
};

function setStatus(text) {
  $("status").textContent = text;
}

function setPanelCollapsed(collapsed) {
  state.panelCollapsed = Boolean(collapsed);
  localStorage.setItem(PANEL_COLLAPSED_KEY, state.panelCollapsed ? "1" : "0");
  document.body.classList.toggle("panel-collapsed", state.panelCollapsed);
  $("panelToggle").textContent = state.panelCollapsed ? "展开菜单" : "收起菜单";
}

function saveDevice() {
  localStorage.setItem(SERVER_KEY, state.server);
  localStorage.setItem("device_id", state.deviceId);
  localStorage.setItem("device_secret", state.deviceSecret);
  localStorage.setItem("device_token", state.token);
  localStorage.setItem("manifest_version", String(state.manifestVersion));
}

function normalizeServer(url) {
  return (url || "").trim().replace(/\/+$/, "");
}

function syncServerFromInput() {
  const value = normalizeServer($("server").value);
  if (!value) throw new Error("后端地址不能为空");
  if (!/^https?:\/\//.test(value)) throw new Error("后端地址需以 http:// 或 https:// 开头");
  state.server = value;
  $("server").value = value;
  saveDevice();
}

async function request(path, options = {}) {
  const headers = options.headers || {};
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const res = await fetch(`${state.server}${path}`, { ...options, headers });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function registerDevice() {
  syncServerFromInput();
  const name = $("name").value.trim() || "Screen-Web";
  const data = await request("/api/devices/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, type: "web", meta: { ua: navigator.userAgent } }),
  });
  state.deviceId = data.device_id;
  state.deviceSecret = data.secret;
  state.token = "";
  state.manifestVersion = 0;
  state.playlist = [];
  state.index = 0;
  saveDevice();
  setStatus(`registered: ${state.deviceId.slice(0, 8)}`);
}

async function loginDevice() {
  syncServerFromInput();
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

function stopRealtime() {
  if (state.heartbeatTimer) {
    clearInterval(state.heartbeatTimer);
    state.heartbeatTimer = null;
  }
  if (state.pollTimer) {
    clearInterval(state.pollTimer);
    state.pollTimer = null;
  }
  if (state.ws) {
    state.ws.close();
    state.ws = null;
  }
}

function connectWs() {
  if (!state.token || state.ws) return;
  const base = state.server.replace("http://", "ws://").replace("https://", "wss://");
  state.ws = new WebSocket(`${base}/ws/device?token=${encodeURIComponent(state.token)}`);

  state.ws.onopen = () => {
    setStatus("ws connected");
    state.ws.send(JSON.stringify({ type: "hello", device_id: state.deviceId, ts: new Date().toISOString() }));

    if (state.heartbeatTimer) clearInterval(state.heartbeatTimer);
    state.heartbeatTimer = setInterval(() => {
      if (state.ws && state.ws.readyState === WebSocket.OPEN) {
        state.ws.send(JSON.stringify({ type: "heartbeat", device_id: state.deviceId, ts: new Date().toISOString() }));
      }
    }, 30000);
  };

  state.ws.onmessage = (ev) => {
    try {
      const msg = JSON.parse(ev.data);
      if (msg.type === "manifest_update") {
        refreshManifest().then(renderCurrent).catch((e) => console.warn(e));
      }
    } catch (_) {}
  };

  state.ws.onclose = () => {
    state.ws = null;
    setStatus("ws closed");
  };
}

async function manualRefresh() {
  syncServerFromInput();
  if (!state.deviceId || !state.token) {
    throw new Error("请先完成设备注册和登录");
  }
  await refreshManifest();
  renderCurrent();
}

async function startPlayback() {
  syncServerFromInput();

  if (!state.deviceId || !state.deviceSecret) {
    throw new Error("请先注册设备");
  }

  if (!state.token) {
    await loginDevice();
  }

  await refreshManifest();
  renderCurrent();
  connectWs();

  if (state.pollTimer) clearInterval(state.pollTimer);
  state.pollTimer = setInterval(async () => {
    try {
      await refreshManifest();
    } catch (e) {
      console.warn("poll failed", e);
    }
  }, 15000);

  state.started = true;
}

async function autoStartIfRegistered() {
  if (!state.deviceId || !state.deviceSecret) return;
  try {
    await startPlayback();
    if (state.playlist.some((item) => item.type === "video")) {
      setPanelCollapsed(true);
    }
  } catch (e) {
    console.warn("auto start failed", e);
    setStatus(`device: ${state.deviceId.slice(0, 8)} @ ${state.server}`);
  }
}

$("register").onclick = () => registerDevice().catch((e) => alert(e.message));
$("login").onclick = () => loginDevice().catch((e) => alert(e.message));
$("start").onclick = () => startPlayback().catch((e) => alert(e.message));
$("refresh").onclick = () => manualRefresh().catch((e) => alert(e.message));
$("saveServer").onclick = () => {
  try {
    stopRealtime();
    state.started = false;
    syncServerFromInput();
    setStatus(`backend: ${state.server}`);
  } catch (e) {
    alert(e.message);
  }
};
$("panelToggle").onclick = () => setPanelCollapsed(!state.panelCollapsed);

$("server").value = state.server;
setPanelCollapsed(state.panelCollapsed);
if (state.deviceId) {
  setStatus(`device: ${state.deviceId.slice(0, 8)} @ ${state.server}`);
} else {
  setStatus(`backend: ${state.server}`);
}

autoStartIfRegistered();

window.addEventListener("beforeunload", () => {
  stopRealtime();
});
