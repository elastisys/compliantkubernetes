"use strict"

var feedback = document.forms.feedback
feedback.hidden = false

feedback.addEventListener("submit", function(ev) {
    ev.preventDefault()

    var page = document.location.pathname
    var data = ev.submitter.getAttribute("data-md-value")

    console.debug(page, data)
    var _paq = window._paq = window._paq || []
    _paq.push(["trackEvent", "Feedback", "Page Feedback Click", page, data])

    feedback.firstElementChild.disabled = true

    var note = feedback.querySelector(
        ".md-feedback__note [data-md-value='" + data + "']"
    )
    if (note)
        note.hidden = false
})
