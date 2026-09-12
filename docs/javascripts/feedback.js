/* Feedback form handler (shared by the EN and AR feedback pages).
 *
 * To deliver submissions straight to the author's inbox, paste the free
 * Web3Forms access key for hend.alkhalifa@gmail.com below. Get it in ~1 minute
 * at https://web3forms.com — enter the email, confirm it, copy the key. Until a
 * key is set, the form opens the visitor's email app (mailto) instead.
 */
(function () {
  var KEY = "YOUR_WEB3FORMS_ACCESS_KEY";

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

      if (KEY && KEY !== "YOUR_WEB3FORMS_ACCESS_KEY") {
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
      } else {
        // mailto fallback (address assembled to reduce scraping)
        var to = ["hend.alkhalifa", "gmail.com"].join("@");
        var body = "Type: " + (data.type || "") + "\nPage: " + (data.page || "") +
                   "\nFrom: " + (data.name || "") + " " + (data.email || "") +
                   "\n\n" + data.message;
        statusEl.textContent = T.opening;
        window.location.href = "mailto:" + to + "?subject=" +
          encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      }
    });
  }

  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
  if (window.document$ && window.document$.subscribe) { window.document$.subscribe(init); }
})();
