
// does not render html on app.route
function addLikeListener() {
    $(".list-group").on("click", ".like-btn", async function() {
        // grab msg.id on parent 'like' div
        let msg_id = $(this).parent().attr("id");
        resp = await $.post(`/messages/${msg_id}/like`)
        $(this).toggleClass("far fas")
    });
};
addLikeListener();