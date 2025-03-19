$(document).ready(function () {

  $("#MicBtn").click(function () {
    $("#Oval").attr("hidden", true);
    $("#Voice").attr("hidden", false);
    eel.allCommands()();
  });

  function doc_keyup(e) {
    if (e.key === 'o' && e.metaKey) {
      $("#Oval").attr("hidden", true);
      $("#Voice").attr("hidden", false);
      eel.allCommands()();
    }
  }
  document.addEventListener('keyup', doc_keyup, false);

  $("#backBtn").click(function () {
    stopListening = true;
    $("#Voice").attr("hidden", true);
    $("#Oval").attr("hidden", false);
    eel.set_stop_listening();
  });

  eel.expose(ShowHood)

  function ShowHood() {
    $("#Oval").attr("hidden", false);
    $("#Voice").attr("hidden", true);
  }

  $("#previousChatsBtn").click(function () {
    $("#Oval").attr("hidden", true);
    $("#Chat").attr("hidden", false);
  });

  $("#ChatbackBtn").click(function () {
    $("#Oval").attr("hidden", false);
    $("#Chat").attr("hidden", true);
  });

  function PlayAssistant(message) {
    if (message != "") {
      eel.chatDisplay(message);
      eel.allChatCommands(message);
      $("#Oval").attr("hidden", true);
      $("#Voice").attr("hidden", false);
      $("#chatbox").val("");
    }
  }

  $(document).ready(function () {
    function sendMessage() {
      let message = $("#chatbox").val().trim();
      
      if (message === "") return;
      
      $("#SendBtn").addClass("clicked");
      setTimeout(() => $("#SendBtn").removeClass("clicked"), 300);

      PlayAssistant(message);
      $("#chatbox").val("");
  
      fetch("/chatbot_responses.json")
        .then(response => response.json())
        .then(data => {
          const chatContainer = $("#chatContainer");
          chatContainer.empty();
  
          if (data.length > 0) {
            const lastChat = data[data.length - 1];
  
            const userMessage = $("<div>").addClass("chat user").text(lastChat.user);
            chatContainer.append(userMessage);
  
            const botMessage = $("<div>").addClass("chat bot").text(lastChat.bot);
            chatContainer.append(botMessage);
          } else {
            chatContainer.text("No chat history available.");
          }
        })
        .catch(error => console.error("Error loading chatbot responses:", error));
  
      setTimeout(function () {
        $("#Voice").attr("hidden", true);
        $("#Chat").attr("hidden", false);
      }, 4000);
    }
  
    $("#SendBtn").click(sendMessage);
  
    $("#chatbox").keypress(function (event) {
      if (event.which === 13 && !event.shiftKey) {
        event.preventDefault();
        $("#SendBtn").click();
      }
    });
  });  


});
