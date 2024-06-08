function mark_as_read(){
    document.addEventListener("click",function(event){
        window.location.href="/admin/mark_as_read/" + event.target.id;
    });
}

function mark_as_unread(){
    document.addEventListener("click",function(event){
        window.location.href="/admin/mark_as_unread/" + event.target.id;
    });
}

function reply(){
    document.addEventListener("click",function(event){
        window.location.href="/admin/reply/" + event.target.id;
    });
}