function setLanguage(lang) {
    console.log('setting ' + lang)
    keys = Object.keys(LOC);
    for (i = 0; i < keys.length; i++) {
        key = keys[i];
        if (key.split("::").length == 1) {
            $("#" + key).html(LOC[key][lang])
        } else if (key.split("::")[1] == "placeholder") {
            $("#" + key.split("::")[0]).attr("placeholder", LOC[key][lang])
        }
    }
    langs = ['en', 'de'];
    langs.splice(langs.indexOf(lang), 1)
    other_lang = langs[0];

    $("#lang-flag").attr('src', "/static/img/" + other_lang + ".svg");
    $("#lang-select").attr("onclick", "setLanguage('" + other_lang + "');");
}