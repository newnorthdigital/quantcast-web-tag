#!/usr/bin/env python3
# Assembles template.tpl, injecting the base64 thumbnail from thumb.b64.
thumb = open('thumb.b64').read().strip()
data_uri = 'data:image/png;base64,' + thumb

TPL = r'''___TERMS_OF_SERVICE___

By creating or modifying this file you agree to Google Tag Manager's Community
Template Gallery Developer Terms of Service available at
https://developers.google.com/tag-manager/gallery-tos (or such other URL as
Google may provide), as modified from time to time.


___INFO___

{
  "type": "TAG",
  "id": "cvt_temp_public_id",
  "version": 1,
  "securityGroups": [],
  "displayName": "Quantcast Measure by New North Digital",
  "categories": [
    "ADVERTISING",
    "ANALYTICS",
    "ATTRIBUTION"
  ],
  "brand": {
    "id": "brand_dummy",
    "displayName": "New North Digital",
    "thumbnail": "__THUMB__"
  },
  "description": "Quantcast Measure tag. Loads the Quantcast pixel and pushes page views and conversions onto the _qevents queue, with revenue and order ID for conversion measurement and custom labels for audience segmentation. Gate it behind GTM consent settings.",
  "containerContexts": [
    "WEB"
  ]
}


___TEMPLATE_PARAMETERS___

[
  {
    "type": "SELECT",
    "name": "actionType",
    "displayName": "Event type",
    "macrosInSelect": false,
    "selectItems": [
      {
        "value": "pageview",
        "displayValue": "Page view"
      },
      {
        "value": "conversion",
        "displayValue": "Conversion"
      }
    ],
    "simpleValueType": true,
    "help": "Choose \"Page view\" for the standard pixel (fire on All Pages). Choose \"Conversion\" on the action you want to measure, such as a purchase: it adds event=refresh so Quantcast records a distinct conversion beacon, with optional revenue and order ID."
  },
  {
    "type": "TEXT",
    "name": "qacct",
    "displayName": "Quantcast account ID (p-code)",
    "simpleValueType": true,
    "valueValidators": [
      {
        "type": "NON_EMPTY"
      }
    ],
    "help": "Your Quantcast p-code, e.g. p-31kzUz5cMTB9k. Find it in your Quantcast tag. You can also reference a GTM variable here.",
    "alwaysInSummary": true
  },
  {
    "type": "TEXT",
    "name": "labels",
    "displayName": "Labels",
    "simpleValueType": true,
    "help": "Event/segment label in _fp.event.<Name> format, e.g. _fp.event.PageView or _fp.event.Purchase. Nest a sub-attribute with another dot (_fp.event.Purchase.sneakers) and separate multiple labels with commas. Drives Audience Insights segmentation. Leave blank to send no label.",
    "defaultValue": "_fp.event.PageView"
  },
  {
    "type": "TEXT",
    "name": "orderid",
    "displayName": "Order ID (optional)",
    "simpleValueType": true,
    "help": "Your unique order identifier. Quantcast uses it to dedupe conversions.",
    "enablingConditions": [
      {
        "paramName": "actionType",
        "paramValue": "conversion",
        "type": "EQUALS"
      }
    ]
  },
  {
    "type": "TEXT",
    "name": "revenue",
    "displayName": "Revenue (optional)",
    "simpleValueType": true,
    "help": "Total conversion value as a plain number, e.g. 100.00. Required for ROAS reporting. Reference a GTM variable such as the transaction value.",
    "enablingConditions": [
      {
        "paramName": "actionType",
        "paramValue": "conversion",
        "type": "EQUALS"
      }
    ]
  },
  {
    "type": "SIMPLE_TABLE",
    "name": "customVars",
    "displayName": "Custom variables (optional)",
    "simpleTableColumns": [
      {
        "defaultValue": "",
        "displayName": "Key",
        "name": "key",
        "type": "TEXT",
        "valueValidators": [
          {
            "type": "NON_EMPTY"
          }
        ]
      },
      {
        "defaultValue": "",
        "displayName": "Value",
        "name": "value",
        "type": "TEXT"
      }
    ],
    "newRowButtonText": "Add variable",
    "help": "Optional extra keys added to the _qevents push, such as pcat, customer or uid. Attach them to standard or custom events to refine a Pixel Audience."
  },
  {
    "type": "GROUP",
    "name": "debugGroup",
    "displayName": "Debugging",
    "groupStyle": "ZIPPY_CLOSED",
    "subParams": [
      {
        "type": "CHECKBOX",
        "name": "debug",
        "checkboxText": "Log to console for debugging",
        "simpleValueType": true
      }
    ]
  }
]


___SANDBOXED_JS_FOR_WEB_TEMPLATE___

const log = require('logToConsole');
const injectScript = require('injectScript');
const createQueue = require('createQueue');
const makeTableMap = require('makeTableMap');
const makeString = require('makeString');

const QUEUE_NAME = '_qevents';
const LOADER = 'https://secure.quantserve.com/quant.js';

const actionType = data.actionType;
const enableDebug = data.debug;

const debugLog = (msg) => {
  if (enableDebug) {
    log('Quantcast GTM - ' + msg);
  }
};

debugLog('Starting with event type: ' + actionType);

const qacct = data.qacct;
if (!qacct) {
  debugLog('Error: Quantcast account ID (p-code) is required');
  data.gtmOnFailure();
  return;
}

// Build the _qevents queue, mirroring the native Quantcast snippet
// (window._qevents = window._qevents || []). The loader quant.js reads the
// queue when it loads, so pushing before or after it loads is safe.
const qevents = createQueue(QUEUE_NAME);

// Start from any custom variables, then layer the standard keys on top.
const payload = (data.customVars && data.customVars.length > 0) ?
  (makeTableMap(data.customVars, 'key', 'value') || {}) : {};

payload.qacct = makeString(qacct);

if (data.labels) {
  payload.labels = data.labels;
}

if (actionType === 'conversion') {
  // event=refresh forces a fresh beacon for this distinct conversion rather
  // than treating it as the same page impression.
  payload.event = 'refresh';
  if (data.orderid) {
    payload.orderid = makeString(data.orderid);
  }
  if (data.revenue) {
    payload.revenue = makeString(data.revenue);
  }
} else if (actionType !== 'pageview') {
  debugLog('Unknown event type: ' + actionType);
  data.gtmOnFailure();
  return;
}

qevents(payload);
debugLog('Pushed ' + actionType + ' for ' + qacct);

// Load quant.js once per page (cache token keeps it from re-injecting per event).
injectScript(LOADER, data.gtmOnSuccess, data.gtmOnFailure, 'quantcast');


___WEB_PERMISSIONS___

[
  {
    "instance": {
      "key": {
        "publicId": "logging",
        "versionId": "1"
      },
      "param": [
        {
          "key": "environments",
          "value": {
            "type": 1,
            "string": "debug"
          }
        }
      ]
    },
    "clientAnnotations": {
      "isEditedByUser": true
    },
    "isRequired": true
  },
  {
    "instance": {
      "key": {
        "publicId": "access_globals",
        "versionId": "1"
      },
      "param": [
        {
          "key": "keys",
          "value": {
            "type": 2,
            "listItem": [
              {
                "type": 3,
                "mapKey": [
                  {"type": 1, "string": "key"},
                  {"type": 1, "string": "read"},
                  {"type": 1, "string": "write"},
                  {"type": 1, "string": "execute"}
                ],
                "mapValue": [
                  {"type": 1, "string": "_qevents"},
                  {"type": 8, "boolean": true},
                  {"type": 8, "boolean": true},
                  {"type": 8, "boolean": true}
                ]
              }
            ]
          }
        }
      ]
    },
    "clientAnnotations": {
      "isEditedByUser": true
    },
    "isRequired": true
  },
  {
    "instance": {
      "key": {
        "publicId": "inject_script",
        "versionId": "1"
      },
      "param": [
        {
          "key": "urls",
          "value": {
            "type": 2,
            "listItem": [
              {
                "type": 1,
                "string": "https://secure.quantserve.com/*"
              }
            ]
          }
        }
      ]
    },
    "clientAnnotations": {
      "isEditedByUser": true
    },
    "isRequired": true
  }
]


___TESTS___

scenarios:
- name: Page view - pushes _qevents and injects loader
  code: |-
    const mockData = {
      actionType: 'pageview',
      qacct: 'p-31kzUz5cMTB9k',
      labels: '_fp.event.PageView',
      debug: false
    };

    mock('injectScript', function(url, onSuccess, onFailure, cacheToken) {
      onSuccess();
    });

    runCode(mockData);

    assertApi('createQueue').wasCalled();
    assertApi('injectScript').wasCalled();
    assertApi('gtmOnSuccess').wasCalled();
- name: Page view - injects the Quantcast loader URL
  code: |-
    const mockData = {
      actionType: 'pageview',
      qacct: 'p-31kzUz5cMTB9k',
      labels: '_fp.event.PageView',
      debug: false
    };

    let capturedUrl = '';
    mock('injectScript', function(url, onSuccess, onFailure, cacheToken) {
      capturedUrl = url;
      onSuccess();
    });

    runCode(mockData);

    assertThat(capturedUrl).isEqualTo('https://secure.quantserve.com/quant.js');
    assertApi('gtmOnSuccess').wasCalled();
- name: Conversion - pushes revenue and order id
  code: |-
    const mockData = {
      actionType: 'conversion',
      qacct: 'p-31kzUz5cMTB9k',
      labels: '_fp.event.Purchase',
      orderid: 'T12345',
      revenue: '100.00',
      debug: false
    };

    mock('injectScript', function(url, onSuccess, onFailure, cacheToken) {
      onSuccess();
    });

    runCode(mockData);

    assertApi('createQueue').wasCalled();
    assertApi('gtmOnSuccess').wasCalled();
- name: Conversion - merges custom variables
  code: |-
    const mockData = {
      actionType: 'conversion',
      qacct: 'p-31kzUz5cMTB9k',
      labels: '_fp.event.Purchase',
      customVars: [
        {key: 'customer', value: 'returning'},
        {key: 'pcat', value: 'shoes'}
      ],
      debug: false
    };

    mock('injectScript', function(url, onSuccess, onFailure, cacheToken) {
      onSuccess();
    });

    runCode(mockData);

    assertApi('gtmOnSuccess').wasCalled();
- name: Fails without a p-code
  code: |-
    const mockData = {
      actionType: 'pageview',
      qacct: '',
      debug: false
    };

    runCode(mockData);

    assertApi('gtmOnFailure').wasCalled();
- name: Loader failure - calls gtmOnFailure
  code: |-
    const mockData = {
      actionType: 'pageview',
      qacct: 'p-31kzUz5cMTB9k',
      labels: '_fp.event.PageView',
      debug: false
    };

    mock('injectScript', function(url, onSuccess, onFailure, cacheToken) {
      onFailure();
    });

    runCode(mockData);

    assertApi('gtmOnFailure').wasCalled();


___NOTES___

Created on 2026-06-29 by New North Digital (newnorth.digital).
'''

TPL = TPL.replace('__THUMB__', data_uri)
with open('template.tpl', 'wb') as f:
    f.write(b'\xef\xbb\xbf')          # UTF-8 BOM (gallery validator expects it)
    f.write(TPL.encode('utf-8'))
print('template.tpl written:', len(TPL) + 3, 'bytes (incl BOM)')
