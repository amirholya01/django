$('#side-menu').metisMenu();

function openNav() {
    document.getElementById("filter-sidebar").style.width = "320px";
}

function closeNav() {
    document.getElementById("filter-sidebar").style.width = "0";
}

function ShowMessage(messageType, messageText, langCode) {
    toastr.options.rtl = false;
    toastr.options.closeButton = false;
    toastr.options.positionClass = 'toast-bottom-full-width';
    switch (messageType) {
        case 'success':
            toastr.success(messageText);
            break;
        case 'warning':
            toastr.warning(messageText);
            break;
        case 'error':
            toastr.error(messageText);
            break;
        case 'info':
            toastr.info(messageText);
            break;
    }
}

function FillPageNumber(page) {
    $('#page-number').val(page);
    SubmitFilterForm();
}

function sendNewAnswerToArticleComment(commentId) {
    document.getElementById("submit-new-comment")
        .scrollIntoView({behavior: 'smooth', block: "center"});
    $('#id_parent_id').val(commentId);
}

function SubmitFilterForm() {
    $('#filter-form').submit();
}

$(document).ready(function () {
    $('[submit-onchange]').on('change', function (e) {
        SubmitFilterForm();
    });
});


function readURL(input, priviewImg) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $(priviewImg).attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("[ImageInput]").change(function () {
    var x = $(this).attr("ImageInput");
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $("[ImageFile=" + x + "]").attr('src', e.target.result);
        };
        reader.readAsDataURL(this.files[0]);
    }
});

function CopyToClipboardByElementId(elementId) {
    var $temp = $("<input>");
    $("body").append($temp);
    var el = $("#" + elementId);
    $temp.val($(el).text()).select();
    document.execCommand("copy");
    $temp.remove();
}

function CopyToClipboardText(text) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val(text).select();
    document.execCommand("copy");
    $temp.remove();
}

$(document).ready(function () {

    var doblock = $("[doblock]");
    var IsBlockUI = doblock.length !== 0;
    // block ui when ajax starts
    if (IsBlockUI) {
        $.getScript("/assets/js/CustomJs/jquery.blockUI.js", function (script, textStatus, jqXHR) {
        });
        $(document).ajaxStart(function () {
            $.blockUI({message: null});
        });
    }

    // set responsive textarea
    var textAreas = $(".animated");
    if (textAreas.length > 0) {
        $.getScript("/js/ResizeTextArea.js", function (script, textStatus, jqXHR) {
        });
    }

    // add tags input when we have data-role='tagsinput' attribute
    var tagsInputs = $("[data-role='tagsinput']");
    if (tagsInputs.length > 0) {
        $('<link/>', {rel: 'stylesheet', type: 'text/css', href: '/assets/TagInput/bootstrap-tagsinput.css'})
            .appendTo('head');
        $.getScript("/assets/TagInput/bootstrap-tagsinput.js", function (script, textStatus, jqXHR) {
        });
    }

    // add auto complete
    var autoComplete = $("[auto-complete]");
    if (autoComplete.length > 0) {
        $('<link/>',
            {
                rel: 'stylesheet',
                type: 'text/css',
                href: 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.5/css/bootstrap-select.min.css'
            }).appendTo('head');
        $.getScript("https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.5/js/bootstrap-select.min.js",
            function (script, textStatus, jqXHR) {
            });
    }

    // add date picker to inputs that has DatePicker Attribute
});

// submit form with filter-search id on change radio buttons
$('input[type=radio].submit-radio').change(function () {
    $("#pageId").val(1);
    $("#filter-search").submit();
});

function open_waiting(selector = 'body', text) {
    $(selector).waitMe({
        effect: 'win8',
        text: text,
        bg: 'rgba(255,255,255,0.7)',
        color: '#000'
    });
}

function close_waiting(selector = 'body') {
    $(selector).waitMe('hide');
}

function reloadPageAfterSeconds(seconds) {
    setTimeout(function () {
        location.reload();
    }, seconds);
}

function AddOwlCarousel(selector, config) {
    $(selector).owlCarousel(config);
}

var cursorPointerElements = $('[cusror-pointer]');
if (cursorPointerElements.length > 0) {
    $.each(cursorPointerElements,
        function (index, value) {
            $(value).css('cursor', 'pointer');
        });
}

function FillCourseCommentParentId(courseId) {
    $('#id_comment_id').val(courseId);
    document.getElementById('submit-course-comment-form').scrollIntoView({
        behavior: 'smooth',
        block: 'center',
        inline: 'center'
    });
}