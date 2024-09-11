$(document).ready(function () {
    const tb_input = $("input[type='text']");
    const btn_recommend = $(".card-container button");
    const output = $(".output-container .output");
    let titles = [];

    $(".output-container").hide();

    $.ajax({
        url: 'http://127.0.0.1:5000/getalltitles',
        method: 'GET',
        dataType: 'json',
        success: function (datas) {
            titles = datas;
            tb_input.autocomplete({
                source: titles,
                delay: 0,
                open: function (event, ui) {
                    adjustAutocomplete("#ui-id-1", tb_input);
                },
                select: function (event, ui) {
                    btn_recommend.focus();
                }
            });
            adjustAutocomplete("#ui-id-1", tb_input);

            function adjustAutocomplete(id, relative) {
                let width = relative.outerWidth();
                let left = tb_input.offset().left;
                $(id).css({
                    "width": width + "px",
                    "max-height": "150px",
                    "left": left + "px",
                    "overflow-y": "auto",
                    "scrollbar-width": "none",
                });
            }
            $(window).on("resize", function () {
                adjustAutocomplete("#ui-id-1", tb_input);
            });
        },
        error: function (e) {
            console.log("Unable to get titles");
        }
    });

    btn_recommend.click(function (e) {
        let result = tb_input.val();

        e.preventDefault();
        tb_input.attr("disabled", true);
        btn_recommend.prop("disabled", true);
        
        $.ajax({
            url: 'http://127.0.0.1:5000/recommend',
            method: 'GET',
            data: { title: result },
            dataType: 'json',
            success: function (datas) {
                $(".output-container").show();

                output.empty();
                datas.forEach(data => {
                    output.append(`<p>${data["title"]}</p>`);
                });
            },
            error: function () {
                console.log("Some sort of recommendation error");
            },
            complete: function () {
                tb_input.removeAttr("disabled");
                btn_recommend.prop("disabled", false);
            },
        });
    });

    // $(".panel-1").hide(); // Temporary
    // $.ajax({
    //     url: 'http://127.0.0.1:5000/recommend',
    //     method: 'GET',
    //     data: { title: "A Beautiful Mind: The Life of Mathematical Genius and Nobel Laureate John Nash" },
    //     dataType: 'json',
    //     success: function (datas) {
    //         const books_container = $(".books-container ul");
    //         datas.forEach(data => {
    //             const a = $("<a></a>");
    //             a.append(`<img src="${data["img-l"]}">`);
    //             a.append(`<span>${data["title"]}</span>`);
    //             a.append(`<span>${data["author"]}</span>`);
    //             a.append(`<span>${data["year"]}</span>`);
    //             const li = $("<li></li>");
    //             li.append(a);
    //             books_container.append(li);
    //         });
    //     },
    // });
});