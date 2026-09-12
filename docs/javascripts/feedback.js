/* Feedback form handler (shared by the EN and AR feedback pages).
 * Submissions are delivered to the author's inbox via Web3Forms
 * (https://web3forms.com). To change the destination, replace the access key
 * below with a new one generated from Web3Forms for the desired email.
 */
(function () {
  var KEY = "0a8856d4-ed4f-45c1-84ca-8c5ace1900a6";

  function init() {
    var form = document.getElementById("feedback-form");
    if (!form || form.dataset.fbBound) return;
    form.dataset.fbBound = "1";
    var statusEl = document.getElementById("feedback-status");
    var ar = (document.documentElement.lang || "").toLowerCase().indexOf("ar") === 0;
    var T = ar ? {
      need: "يرجى كتابة رسالة أولًا.",
      sending: "جارٍ الإرسال…",
      ok: "شكرًا! أُرسلت ملاحظتك.",
      err: "عذرًا، حدث خطأ — يرجى فتح مشكلة على GitHub بدلًا من ذلك.",
      net: "خطأ في الشبكة — يرجى المحاولة لاحقًا.",
      opening: "يجري فتح تطبيق البريد لديك…",
      subject: "[ملاحظة على الكتاب] "
    } : {
      need: "Please write a message first.",
      sending: "Sending…",
      ok: "Thank you! Your feedback was sent.",
      err: "Sorry, something went wrong — please open a GitHub issue instead.",
      net: "Network error — please try again later.",
      opening: "Opening your email app…",
      subject: "[Book feedback] "
    };

    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      var data = Object.fromEntries(new FormData(form).entries());
      if (data.botcheck) return;                       // spam honeypot
      if (!data.message || !data.message.trim()) { statusEl.textContent = T.need; return; }
      var subject = T.subject + (data.type || "Comment") + (data.page ? " — " + data.page : "");

      statusEl.textContent = T.sending;
      try {
        var res = await fetch("https://api.web3forms.com/submit", {
          method: "POST",
          headers: { "Content-Type": "application/json", "Accept": "application/json" },
          body: JSON.stringify({
            access_key: KEY, subject: subject,
            from_name: data.name || "Website visitor", replyto: data.email || "",
            name: data.name || "", email: data.email || "",
            page: data.page || "", type: data.type || "", message: data.message
          })
        });
        var j = await res.json();
        if (j.success) { form.reset(); statusEl.textContent = T.ok; }
        else { statusEl.textContent = T.err; }
      } catch (err) { statusEl.textContent = T.net; }
    });
  }

  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
  if (window.document$ && window.document$.subscribe) { window.document$.subscribe(init); }
})();
