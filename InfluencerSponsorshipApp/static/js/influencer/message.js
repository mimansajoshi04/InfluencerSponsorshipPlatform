function mark_as_read(){
    document.addEventListener("click",function(event){
        window.location.href="/influencer/mark_as_read/" + event.target.id;
    });
}

function mark_as_unread(){
    document.addEventListener("click",function(event){
        window.location.href="/influencer/mark_as_unread/" + event.target.id;
    });
}

function reply(){
    document.addEventListener("click",function(event){
        window.location.href="/influencer/reply/" + event.target.id;
    });
}

function send_message(){
    window.location.href = "/influencer/send_message";
  }