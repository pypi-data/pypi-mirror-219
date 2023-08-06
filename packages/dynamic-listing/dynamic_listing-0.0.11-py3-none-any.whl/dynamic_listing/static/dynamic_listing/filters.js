var addFiltersToDynamicListingApp = function () {
  var dateRangeFilters


  function submit(form) {
    var data = Array.from(new FormData(form))
            .filter(function ([k, v]) {
              return v
            }),
        params = new URLSearchParams(data)

    location.href = location.origin + location.pathname + "?" + params.toString()
  }

  function initDateRangeFilters() {
    $('[data-date-range-filter="true"]').daterangepicker({}, function (start, end) {
      var $from = this.element.siblings(`[data-range-from="${this.element.data('name')}"]`),
          $to = this.element.siblings(`[data-range-to="${this.element.data('name')}"]`)

      $from.val(start.format('MM/DD/YYYY'))
      $to.val(end.format('MM/DD/YYYY'))
      submit(this.element.closest('form')[0])
    })
  }

  function initFilterForms() {
    initDateRangeFilters()

    $(document)
        .on('change', '[data-instant-filter="true"]', function (e) {
          submit($(this).closest('form')[0])
        })
        .on('submit', '[data-toggle="filters"]', function (e) {
          e.preventDefault()
          submit(this)
        })
        .on('click', '[data-reset-filters="true"]', function (e) {
          e.preventDefault()
          location.href = location.origin + location.pathname
        })
        .on('search', 'input[type="search"]', function (e) {
          submit($(this).closest('form')[0])
        })

  }


  return {
    init() {
      dateRangeFilters = $('[data-date-range-filter="true"]')
      initFilterForms()
    }
  }
}()

document.addEventListener('DOMContentLoaded', addFiltersToDynamicListingApp.init);
if (document.readyState !== 'loading' && document.body)
  addFiltersToDynamicListingApp.init();