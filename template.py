css = """
<style>
.chat-message {
    padding: 2.0rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #f3f6f4
}
.chat-message.bot {
    background-color: #cbebcb
}
.chat-message .avatar {
  width: 15%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #000000;
}
"""
bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.imgur.com/usMWRaF.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.imgur.com/QXPPsEJ.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
"""