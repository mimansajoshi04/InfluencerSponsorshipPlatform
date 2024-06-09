function mark_as_read(){
    document.addEventListener("click",function(event){
        window.location.href="/sponsor/mark_as_read/" + event.target.id;
    });
}

function mark_as_unread(){
    document.addEventListener("click",function(event){
        window.location.href="/sponsor/mark_as_unread/" + event.target.id;
    });
}

function reply(){
    document.addEventListener("click",function(event){
        window.location.href="/sponsor/reply/" + event.target.id;
    });
}

function send_message(){
    window.location.href = "/sponsor/send_message";
  }
