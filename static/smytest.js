$(document).ready(function () {
    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        } 
    });

    $.ajax({
        url: "/api/models/",
        type: "GET",
        dataType : "json",
        success: function (json) {
            var $div_models = $(".models");
            $.each(json.models, function (index, value) {
                $div_models.append("<a href=\"javascript:getModelStruct('" + value.name + "')\">" + value.title + "</a><br>");
            });
        },
    });
 
    $("#add_form").submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: "/api/add/",
            type: "POST",
            data: $("#add_form").serialize(),
            dataType: "json",
            success: function (json) {
                $(".form_error").remove();
                if (json.success) {
                    getModelStruct($("input[name='model_name']").val());
                }
                else {
                    if (json.error) {
                        var $input;
                        $.each(json.error, function (index, value) {
                            $("#" + value.field).before("<p class='form_error'>" + value.text + "</p>");
                        });
                    }
                }
            },
        });
    });
    
    $(".data").on("click", ".data_row td", function () {
        if (jQuery(this).children("input").length) {
            jQuery(this).children("input").show();
            jQuery(this).children("span").hide();
        }
    });
    
    $(".data").on("keypress", ".modify", function (event) {
        if (event.which == 13) {
            jQuery(this).hide();
            jQuery(this).parent().children("span").show();
            modifyField({
                model_name: $("input[name='model_name']").val(),
                id: jQuery(this).parent().parent().attr("name"),
                name: jQuery(this).attr("name"),
                value: jQuery(this).val(),
            });
        }
    });

    var modifyField = function (data) {
        $.ajax({
            url: "/api/modify/",
            type: "POST",
            data: data,
            dataType: "json",
            success: function (json) {
                if (json.success) {
                    getModelStruct($("input[name='model_name']").val());
                }
            },
        });        
    };
});

var getModelStruct = function (model_name) {
    $.ajax({
        url: "/api/model/",
        type: "POST",
        data: {
            name: model_name,
        },
        dataType: "json",
        success: function (json) {
            var $table_data = $(".data");
            $table_data.empty();
            var $tr = "";
            var $input = "";
            $.each(json.head, function (index, value) {
                $tr += "<th>" + value.title + "</th>";
            })
            $table_data.append("<tr>" + $tr + "</tr>");
            $.each(json.data, function (index, value) {
                $tr = "";
                $.each(json.head, function (indexH, valueH) {
                    $input = "";                    
                    if (valueH.type) {
                        $input = "<input name='" + valueH.name + "' type='" + valueH.type + "' value='" + value[valueH.name] + "' class='modify' hidden>";
                    }
                    $tr += "<td><span class='value'>" + value[valueH.name] + "</span>" + $input + "</td>";
                });
                $table_data.append("<tr class='data_row' name='" + value["id"] + "'>" + $tr + "</tr>");
            });
            var $form = $("#add_form");
            $form.empty();
            var $fieldset = ""
            $.each(json.head, function (index, value) {
                if (value.type) {
                    $fieldset += "<div id='" + value.name + "'>" + value.title + "<input name='" + value.name + "' type='" + value.type + "'></div></br>";
                }
            });
            if ($fieldset != "") {
                $fieldset += "<input name='model_name' type='hidden' value='" + model_name + "'>";
                $fieldset += "<input type='submit' value='Добавить'>";
                $form.append("<fieldset>" + $fieldset + "</fieldset>");
            }
        }
    });
}
