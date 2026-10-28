const form = document.getElementById('chatForm');
const input = document.getElementById('message');
const area = document.getElementById('chatArea');
const welcome = document.getElementById('welcome');
const sendBtn = document.getElementById('sendBtn');
const language = document.getElementById('language');

function addMessage(text, who) {
  if (welcome) welcome.style.display = 'none';
  const row = document.createElement('div');
  row.className = `message-row ${who}`;
  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  avatar.textContent = who === 'user' ? 'You' : '✦';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  row.append(avatar, bubble);
  area.appendChild(row);
  area.scrollTop = area.scrollHeight;
}
async function sendMessage(text) {
  const trimmed = text.trim();
  if (!trimmed) return;
  addMessage(trimmed, 'user');
  input.value = '';
  input.style.height = 'auto';
  sendBtn.disabled = true;
  const pending = document.createElement('div');
  pending.className = 'message-row bot pending';
  pending.innerHTML = '<div class="message-avatar">✦</div><div class="bubble"><span class="typing"><i></i><i></i><i></i></span> Thinking…</div>';
  area.appendChild(pending);
  area.scrollTop = area.scrollHeight;
  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: trimmed, language: language.value})
    });
    const data = await response.json();
    pending.remove();
    addMessage(data.reply || 'Sorry, I could not prepare a response.', 'bot');
  } catch (e) {
    pending.remove();
    addMessage('Could not reach the local server. Check that Flask is running and try again.', 'bot');
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}
form.addEventListener('submit', e => { e.preventDefault(); sendMessage(input.value); });
input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
});
input.addEventListener('input', () => { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 140) + 'px'; });
document.querySelectorAll('.suggestion').forEach(btn => btn.addEventListener('click', () => sendMessage(btn.dataset.prompt)));
document.getElementById('newChat').addEventListener('click', () => {
  area.innerHTML = '';
  if (welcome) { welcome.style.display = 'flex'; area.appendChild(welcome); }
  input.value = '';
});
