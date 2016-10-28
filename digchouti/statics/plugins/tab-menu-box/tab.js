/**
 * Created by wupeiqi on 16/8/9.
 */
/*
tab菜单
 */
function BindTabMenu(title, body) {
    $(title).children().bind("click", function () {
        var $menu = $(this);
        var $content = $(body).find('div[content="' + $(this).attr("content-to") + '"]');
        $menu.addClass('current').siblings().removeClass('current');
        $content.removeClass('hide').siblings().addClass('hide');
    });
}