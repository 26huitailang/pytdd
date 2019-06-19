// todo: 触发不了
window.Superlists = {};
window.Superlists.initialize = function () {
  $('input[name="text"]').on('keypress', function () {
    $('.has-error').hide();
  });
};

QUnit.test("errors should be hidden on keypress", function (assert) {
  window.Superlists.initialize();
  $('input[name="text"]').trigger("keypress");
  // $(".has-error").hide();
  assert.equal($(".has-error").is(":visible"), false);
});

QUnit.test("errors not be hidden unless there is a keypress", function (assert) {
  window.Superlists.initialize();
  assert.equal($(".has-error").is(":visible"), true);
})
