"use strict"

var DynamicChartHandlersInitialized = false
window.DynamicChartDataStore = {}
window.DynamicChartDataStoreID = 0

var DynamicChartUtils = function () {
  return {
    deepExtend: function (out) {
      out = out || {}

      for (var i = 1; i < arguments.length; i++) {
        var obj = arguments[i]
        if (!obj) continue

        for (var key in obj) {
          if (!obj.hasOwnProperty(key)) {
            continue
          }

          // based on https://javascriptweblog.wordpress.com/2011/08/08/fixing-the-javascript-typeof-operator/
          if (Object.prototype.toString.call(obj[key]) === '[object Object]') {
            out[key] = DynamicChartUtils.deepExtend(out[key], obj[key])
            continue
          }

          out[key] = obj[key]
        }
      }

      return out
    },
    data: function (el) {
      return {
        set: function (name, data) {
          if (!el) {
            return;
          }

          if (el.customDataTag === undefined) {
            window.DynamicChartDataStoreID++;
            el.customDataTag = window.DynamicChartDataStoreID;
          }

          if (window.DynamicChartDataStore[el.customDataTag] === undefined) {
            window.DynamicChartDataStore[el.customDataTag] = {};
          }

          window.DynamicChartDataStore[el.customDataTag][name] = data;
        },

        get: function (name) {
          if (!el) {
            return;
          }

          if (el.customDataTag === undefined) {
            return null;
          }

          return this.has(name) ? window.DynamicChartDataStore[el.customDataTag][name] : null;
        },

        has: function (name) {
          if (!el) {
            return false;
          }

          if (el.customDataTag === undefined) {
            return false;
          }

          return !!(window.DynamicChartDataStore[el.customDataTag] && window.DynamicChartDataStore[el.customDataTag][name]);
        },

        remove: function (name) {
          if (el && this.has(name)) {
            delete window.DynamicChartDataStore[el.customDataTag][name];
          }
        }
      };
    },
  }
}()

var DynamicChart = function (element, options) {
  var the = this

  if (typeof element === "undefined" || element === null) {
    return
  }
  var defaultOptions = {
    type: 'line',
    data: {},
    options: {},
    plugins: [],
  }

  var _construct = function () {
    if (DynamicChartUtils.data(element).has('chart') === true) {
      the = DynamicChartUtils.data(element).get('chart')
    } else {
      _init()
    }
  }

  var _initChartJs = function () {
    the.chart = new Chart(the.element.getContext('2d'), the.data);
  }

  var _init = function () {
    the.options = DynamicChartUtils.deepExtend({}, defaultOptions, options)
    the.element = element
    the.data = JSON.parse(element.getAttribute('data-chart'))
    console.log(the.data)
    the.element.setAttribute('data-dynamic-chart', 'true')
    _initChartJs()

    DynamicChartUtils.data(the.element).set('chart', the)
  }

  _construct()

  var _setData = function () {
    var labels = ''
  }
}


DynamicChart.getInstance = function (element) {
  var chart

  if (!element) return null

  if (DynamicChartUtils.data(element).has('chart')) {
    return DynamicChartUtils.data(element).get('chart')
  }

  chart = element.closest('.chart')
  if (chart) {
    if (DynamicChartUtils.data(chart).has('chart')) {
      return DynamicChartUtils.data(chart).get('chart')
    }
  }

  return null
}

DynamicChart.initHandlers = function () {

}

DynamicChart.createInstances = function (selector = '[data-dynamic-chart="true"]') {
  var elements = document.querySelectorAll(selector)
  if (elements && elements.length > 0) {
    for (var i = 0, len = elements.length; i < len; i++) {
      new DynamicChart(elements[i]);
    }
  }
}
DynamicChart.init = function () {
  DynamicChart.createInstances()

  if (DynamicChartHandlersInitialized === false) {
    DynamicChart.initHandlers()

    DynamicChartHandlersInitialized = true
  }
}


// On document ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", function () {
    DynamicChart.init();
  });
} else {
  DynamicChart.init();
}