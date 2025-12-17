// ======= UI helper =======
const $ = (id) => document.getElementById(id);

// ======= Modal controls =======
function openLogin(){ $('modalLogin').style.display = 'flex'; }
function closeLogin(){ $('modalLogin').style.display = 'none'; }
function openSignup(){ $('modalSignup').style.display = 'flex'; }
function closeSignup(){ $('modalSignup').style.display = 'none'; }

// ======= Simple swap & clear =======
function swapPlaces(){
  const s = $('start'), e = $('end');
  [s.value, e.value] = [e.value, s.value];
  s.focus();
}

function clearFields(){
  $('start').value = '';
  $('end').value = '';
  $('busBody').innerHTML = `<div class="placeholder">Awaiting backend data...</div>`;
  $('metroBody').innerHTML = `<div class="placeholder">Backend will inject metro data here.</div>`;
  $('trafficBody').innerHTML = `<div class="placeholder">Traffic status will appear here</div>`;
  $('altBody').innerHTML = `<div class="placeholder">Alternatives will appear here</div>`;
  $('etaBody').innerHTML = `<div class="placeholder">ETA will appear here</div>`;
  $('start').focus();
}

// ======= Login / Signup (frontend-only) =======
function loginUser(){
  const email = $('loginEmail').value.trim();
  const pass = $('loginPass').value.trim();
  if(!email || !pass){
    alert('Please enter email and password');
    return;
  }
  setLoggedIn(email);
  closeLogin();
}

function signupUser(){
  const name = $('signName').value.trim();
  const email = $('signEmail').value.trim();
  const pass = $('signPass').value.trim();

  if(!name || !email || !pass){
    alert('Please fill all fields');
    return;
  }
  setLoggedIn(email, name);
  closeSignup();
}

function setLoggedIn(email, name){
  $('navActions').innerHTML = `
    <div class="user-pill">
      <i class="fa-solid fa-user"></i>
      <span class="user-email">${name ? name : email}</span>
      <button class="btn ghost" onclick="logout()" style="margin-left:12px">
        <i class="fa-solid fa-right-from-bracket"></i> Logout
      </button>
    </div>
  `;
}

function logout(){
  $('navActions').innerHTML = `
    <button class="btn ghost" onclick="openLogin()">
      <i class="fa-solid fa-right-to-bracket"></i> Login
    </button>
    <button class="btn primary" onclick="openSignup()">
      <i class="fa-solid fa-user-plus"></i> Sign Up
    </button>
  `;
}

// ======= Skeleton Helpers =======
function showLoadingSkeletons(){
  const ids = ['busBody','metroBody','trafficBody','altBody','etaBody'];
  ids.forEach(id=>{
    const el = $(id);
    if(el){
      el.innerHTML = `
        <div style="width:100%;display:flex;flex-direction:column;gap:10px">
          <div class="skeleton" style="width:60%"></div>
          <div class="skeleton" style="width:90%"></div>
          <div class="skeleton" style="width:40%"></div>
        </div>
      `;
    }
  });
}

// ======= RANDOM TRAFFIC + ETA (FRONTEND ONLY) =======
function generateTrafficETA(){
  const trafficLevels = [
    { level: "LOW", color: "#2ecc71", etaMin: 20, etaMax: 30 },
    { level: "MODERATE", color: "#f1c40f", etaMin: 30, etaMax: 45 },
    { level: "HIGH", color: "#e74c3c", etaMin: 45, etaMax: 70 }
  ];

  const selected = trafficLevels[Math.floor(Math.random() * trafficLevels.length)];
  const eta = Math.floor(Math.random() * (selected.etaMax - selected.etaMin + 1)) + selected.etaMin;

  $('trafficBody').innerHTML = `
    <div class="traffic-status">
      Traffic is -
      <b style="color:${selected.color}">${selected.level}</b>
    </div>
  `;

  $('etaBody').innerHTML = `
    <div class="eta-box">
      Estimated Arrival Time:
      <b>${eta} mins</b>
    </div>
  `;

  let suggestion =
    selected.level === "HIGH"
      ? "Metro Recommended 🚇 (Heavy traffic)"
      : "Bus / Cab Recommended 🚌🚕";

  $('altBody').innerHTML = `
    <div class="alt-box">
      ${suggestion}<br/>
      <small>Cab options: Ola · Uber · Rapido</small>
    </div>
  `;
}

// ======= BUS SEARCH =======
async function searchRoute(){
  const start = $('start').value.trim();
  const end = $('end').value.trim();

  if(!start || !end){
    alert('Enter both start and destination');
    return;
  }

  document.querySelector(".results-wrap").style.display = "block";

  try {
    const response = await fetch("/bus-route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start, end })
    });

    const data = await response.json();

    if (data.error) {
      $('busBody').innerHTML = `<div class="placeholder">${data.error}</div>`;
    } else {
      $('busBody').innerHTML = `
        <pre style="white-space: pre-wrap; font-size:14px; line-height:1.6">
${data.result}
        </pre>
      `;
    }

  } catch {
    $('busBody').innerHTML = `<div class="placeholder">Backend error</div>`;
  }
}

// ======= METRO SEARCH =======
async function searchMetroRoute(){
  const start = $('start').value.trim();
  const end = $('end').value.trim();

  if(!start || !end){
    $('metroBody').innerHTML = `<div class="placeholder">Enter start and destination</div>`;
    return;
  }

  try {
    const response = await fetch("/metro-route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start, end })
    });

    const data = await response.json();

    if (data.error) {
      $('metroBody').innerHTML = `<div class="placeholder">${data.error}</div>`;
    } else {
      let html = '<pre style="white-space: pre-wrap; font-size:14px; line-height:1.6">';
      data.lines.forEach(line => html += line + '\n');
      html += '</pre>';
      $('metroBody').innerHTML = html;
    }

  } catch {
    $('metroBody').innerHTML = `<div class="placeholder">Backend error</div>`;
  }
}

// ======= MAIN SEARCH =======
async function searchAll(){
  showLoadingSkeletons();
  await searchRoute();
  await searchMetroRoute();
  generateTrafficETA(); // 👈 frontend-only magic
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  document.querySelector(".results-wrap").style.display = "none";
});
