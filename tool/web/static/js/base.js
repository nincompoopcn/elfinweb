function replaceParamVal(paramName, replaceWith) {
    var oUrl = window.location.href;
    var re = eval('/(' + paramName + '=)([^&]*)/gi');
    var nParam = paramName + '=' + replaceWith;
    if (oUrl.match(re)) {
        return oUrl.replace(re, nParam);
    } else {
        if (oUrl.match('[\?]')) { 
            return oUrl + '&' + nParam; 
        } else { 
            return oUrl + '?' + nParam; 
        } 
    }
}

function validateFormError(elem, errorVal) {
    if ($(elem).val() == errorVal) {
        $(elem).addClass('uk-form-danger');
        return true;
    } else {
        $(elem).removeClass('uk-form-danger');
        return false;
    }
}

function getToday() {
    var now = new Date();

    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    var day = now.getDate();

    var today = year + "-";

    if (month < 10) today += "0";
    today += month + "-";

    if (day < 10) today += "0";
    today += day;

    return today; 
}