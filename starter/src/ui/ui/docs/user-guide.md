<!-- omit in toc -->
# Oracle Digital Assistant Native Client SDK for Web
<!-- omit in toc -->
## Release 24.12

Use Oracle Digital Assistant Native Client SDK for Web to add live messaging to your website or web app.

- [Installation](#installation)
  - [HTML Script Tag](#html-script-tag)
  - [Import the SDK Library in JavaScript](#import-the-sdk-library-in-javascript)
  - [Import the Library Using the Asynchronous Module Definition API](#import-the-library-using-the-asynchronous-module-definition-api)
- [Browser Support](#browser-support)
- [SDK Security](#sdk-security)
  - [Channel with Client Auth Disabled](#channel-with-client-auth-disabled)
  - [Channel with Client Auth Enabled](#channel-with-client-auth-enabled)
  - [JWT Token](#jwt-token)
- [Settings](#settings)
  - [Network Configuration](#network-configuration)
  - [Feature Flags](#feature-flags)
  - [Functionality Configuration](#functionality-configuration)
  - [Layout Modification](#layout-modification)
  - [Custom Colors](#custom-colors)
  - [Custom Icons](#custom-icons)
  - [Custom Text](#custom-text)
  - [Keyboard Shortcuts - Hotkeys](#keyboard-shortcuts---hotkeys)
  - [Customizing CSS Classes](#customizing-css-classes)
- [Enums](#enums)
  - [WebSDK.EVENT](#websdkevent)
  - [WebSDK.SPEECH\_LOCALE](#websdkspeech_locale)
  - [WebSDK.THEME](#websdktheme)
  - [WebSDK.TTS](#websdktts)
- [Methods](#methods)
  - [connect()](#connect)
  - [connect(config)](#connectconfig)
  - [disconnect()](#disconnect)
  - [isConnected()](#isconnected)
  - [endChat()](#endchat)
  - [openChat()](#openchat)
  - [closeChat()](#closechat)
  - [isChatOpened()](#ischatopened)
  - [showWidget()](#showwidget)
  - [hideWidget()](#hidewidget)
  - [destroy()](#destroy)
  - [sendAttachment(file)](#sendattachmentfile)
  - [sendMessage(message, options)](#sendmessagemessage-options)
  - [sendUserTypingStatus(status, userText)](#sendusertypingstatusstatus-usertext)
  - [updateUser(userDetails)](#updateuseruserdetails)
  - [setUserAvatar(userAvatar)](#setuseravataruseravatar)
  - [setAgentDetails(agentDetails)](#setagentdetailsagentdetails)
  - [getAgentDetails()](#getagentdetails)
  - [getSuggestions(query)](#getsuggestionsquery)
  - [startVoiceRecording(onSpeechRecognition, onSpeechNetworkChange, options)](#startvoicerecordingonspeechrecognition-onspeechnetworkchange-options)
  - [stopVoiceRecording()](#stopvoicerecording)
  - [setSpeechLocale(locale)](#setspeechlocalelocale)
  - [setPrimaryChatLanguage(languageTag)](#setprimarychatlanguagelanguagetag)
  - [setSkillVoices(voices)](#setskillvoicesvoices)
  - [setTTSService(service)](#setttsserviceservice)
  - [getTTSVoices()](#getttsvoices)
  - [setTTSVoice(voices)](#setttsvoicevoices)
  - [getTTSVoice()](#getttsvoice)
  - [speakTTS(phrase)](#speakttsphrase)
  - [cancelTTS()](#canceltts)
  - [setDelegate(delegate)](#setdelegatedelegate)
  - [getConversationHistory()](#getconversationhistory)
  - [clearConversationHistory(userId, shouldClearWidget)](#clearconversationhistoryuserid-shouldclearwidget)
  - [clearAllConversationsHistory(shouldClearWidget)](#clearallconversationshistoryshouldclearwidget)
  - [getUnreadMessagesCount()](#getunreadmessagescount)
  - [setAllMessagesAsRead()](#setallmessagesasread)
  - [setUserInputMessage(text)](#setuserinputmessagetext)
  - [setUserInputPlaceholder(text)](#setuserinputplaceholdertext)
  - [showTypingIndicator()](#showtypingindicator)
  - [setWebViewConfig(webViewConfig)](#setwebviewconfigwebviewconfig)
  - [setChatBubbleIconHeight(height)](#setchatbubbleiconheightheight)
  - [setChatBubbleIconWidth(width)](#setchatbubbleiconwidthwidth)
  - [setChatBubbleIconSize(width, height)](#setchatbubbleiconsizewidth-height)
  - [setFont(font)](#setfontfont)
  - [setFontFamily(fontFamily)](#setfontfamilyfontfamily)
  - [setFontSize(fontSize)](#setfontsizefontsize)
  - [setHeight(height)](#setheightheight)
  - [setWidth(width)](#setwidthwidth)
  - [setSize(width, height)](#setsizewidth-height)
  - [setMessagePadding(padding)](#setmessagepaddingpadding)
  - [setTextColor(color)](#settextcolorcolor)
  - [setTextColorLight(color)](#settextcolorlightcolor)
- [Events](#events)
  - [ready](#ready)
  - [destroy](#destroy-1)
  - [message:received](#messagereceived)
  - [message:sent](#messagesent)
  - [message](#message)
  - [networkstatuschange](#networkstatuschange)
  - [typing](#typing)
  - [unreadCount](#unreadcount)
  - [widget:opened](#widgetopened)
  - [widget:closed](#widgetclosed)
  - [widget:show](#widgetshow)
  - [widget:hide](#widgethide)
  - [click:audiotoggle](#clickaudiotoggle)
  - [click:erase](#clickerase)
  - [click:voicetoggle](#clickvoicetoggle)
  - [chatlanguagechange](#chatlanguagechange)
  - [chatend](#chatend)
  - [TTSStart](#ttsstart)
  - [TTSStop](#ttsstop)
- [Features](#features)
  - [Autocomplete](#autocomplete)
  - [Auto-Submit](#auto-submit)
  - [Replacing Previous Edit-Form](#replacing-previous-edit-form)
  - [Delegation](#delegation)
    - [beforeDisplay](#beforedisplay)
    - [beforeSend](#beforesend)
    - [beforePostbackSend](#beforepostbacksend)
    - [beforeEndConversation](#beforeendconversation)
    - [render](#render)
  - [Embedded Mode](#embedded-mode)
  - [Headless SDK](#headless-sdk)
  - [In-Widget Webview](#in-widget-webview)
  - [Long Polling](#long-polling)
  - [Multi-Lingual Chat](#multi-lingual-chat)
    - [Enable the Language Menu](#enable-the-language-menu)
    - [Disable Language Menu](#disable-language-menu)
    - [Language Detection](#language-detection)
    - [Multi-Lingual Chat Quick Reference](#multi-lingual-chat-quick-reference)
  - [Text-to-Speech](#text-to-speech)
  - [Speech Synthesis Service Injection](#speech-synthesis-service-injection)
    - [Speech Synthesis Service Interface](#speech-synthesis-service-interface)
  - [Voice Recognition](#voice-recognition)
  - [Absolute and Relative Timestamps](#absolute-and-relative-timestamps)
  - [Cross-Tab Conversation Synchronization](#cross-tab-conversation-synchronization)
  - [End Conversation Session](#end-conversation-session)
  - [Default Client Responses](#default-client-responses)
  - [Custom Message Rendering](#custom-message-rendering)
  - [Live Agent Typing Indicator](#live-agent-typing-indicator)
- [Customization](#customization)
  - [Add Avatar Icons to Messages](#add-avatar-icons-to-messages)
  - [Card Cardinal Utterance for Card Messages](#card-cardinal-utterance-for-card-messages)
  - [Change Header Buttons Icons](#change-header-buttons-icons)
  - [Draggable Launch Button and widget](#draggable-launch-button-and-widget)
  - [Feedback Message's Rating Gauge](#feedback-messages-rating-gauge)
  - [Focus First Action of Skill Message](#focus-first-action-of-skill-message)
  - [Format Message Timestamps](#format-message-timestamps)
  - [Open Links](#open-links)
  - [Relative Timestamps](#relative-timestamps)
  - [Restrict Attachment Types](#restrict-attachment-types)
    - [Custom Share Menu Items](#custom-share-menu-items)
- [Message Model](#message-model)
  - [Base Types](#base-types)
    - [Action](#action)
      - [PostbackAction](#postbackaction)
      - [CallAction](#callaction)
      - [UrlAction](#urlaction)
      - [ShareAction](#shareaction)
      - [LocationAction](#locationaction)
      - [SubmitFormAction](#submitformaction)
      - [PopupAction](#popupaction)
    - [Attachment](#attachment)
    - [Card](#card)
    - [Location](#location)
    - [Heading](#heading)
    - [Field](#field)
    - [SelectFieldOption](#selectfieldoption)
    - [Read Only Field](#read-only-field)
      - [Text Field](#text-field)
      - [Link Field](#link-field)
      - [Media Field](#media-field)
      - [Action Field](#action-field)
    - [Editable Field](#editable-field)
      - [SingleSelect](#singleselect)
      - [MultiSelect](#multiselect)
      - [DatePicker](#datepicker)
      - [TimePicker](#timepicker)
      - [Toggle](#toggle)
      - [TextInput](#textinput)
      - [NumberInput](#numberinput)
    - [Row](#row)
    - [Form](#form)
    - [FormRow](#formrow)
    - [Column](#column)
    - [PaginationInfo](#paginationinfo)
    - [EventContextProperties](#eventcontextproperties)
  - [Conversation Messages](#conversation-messages)
  - [Message](#message-1)
  - [User Message](#user-message)
    - [User Text Message](#user-text-message)
    - [User Attachment Message](#user-attachment-message)
    - [User Location Message](#user-location-message)
    - [User Postback Message](#user-postback-message)
    - [User InboundEvent Message](#user-inboundevent-message)
    - [User Form Submission Message](#user-form-submission-message)
  - [Skill Message](#skill-message)
    - [Skill Text Message](#skill-text-message)
    - [Skill Attachment Message](#skill-attachment-message)
    - [Skill Location Message](#skill-location-message)
    - [Skill Postback Message](#skill-postback-message)
    - [Skill Card Message](#skill-card-message)
    - [Skill Feedback Message](#skill-feedback-message)
    - [Skill Table Message](#skill-table-message)
    - [Skill Form Message](#skill-form-message)
    - [Skill Table-Form Message](#skill-table-form-message)
    - [Skill Edit-Form Message](#skill-edit-form-message)
    - [Skill OutboundEvent Message](#skill-outboundevent-message)
    - [Skill Raw Message](#skill-raw-message)
- [Limitations](#limitations)

## Installation

### HTML Script Tag

1. First, save `web-sdk.js` in your project directory. Keep note of its location.
2. Create a JavaScript file with the following function that initializes the SDK. Replace the `<Server URI>` with the hostname of the ODA instance, and replace `<Channel ID>` with the channel ID of the Web Channel to which you want to connect. You can pass `<User ID>` to identify a user. The SDK generates a random ID if you skip passing the ID.
```js
// settings.js
var chatSettings = {
    URI: '<Server URI>',
    channelId: '<Channel ID>',
    userId: '<User ID>'
};

function initSDK(name) {
    // If WebSDK is not available, reattempt later
    if (!document || !WebSDK) {
        setTimeout(function() {
            initSDK(name);
        }, 2000);
        return;
    }

    // Default name is Bots
    if (!name) {
        name = 'Bots';
    }

    setTimeout(function() {
        var Bots = new WebSDK(chatSettings);    // Initiate library with configuration

        var isFirstConnection = true;
        Bots.on(WebSDK.EVENT.WIDGET_OPENED, function() {
            if (isFirstConnection) {
                Bots.connect()                          // Connect to server
                    .then(function() {
                        console.log('Connection Successful');
                    })
                    .catch(function(reason) {
                        console.log('Connection failed');
                        console.log(reason);
                    });
                   isFirstConnection = false;
            }
        });

        window[name] = Bots;
    }, 0);
}
```
3. Link the web-sdk library and the above JS file (`settings.js`) on your HTML page. Replace `<WebSDK URL>` with the location of `web-sdk.js`, and `<WebSDK namespace>` with a name for the library, typically `Bots`. The library will be referred by that name when used to make the API calls.
```html
<head>
   <script src="settings.js"></script>
   <script src="<WebSDK URL>" onload="initSDK('<WebSDK namespace>')"></script>
</head>
```

You need to make a few minor modifications if you're connecting to a channel with client authentication enabled. Along with passing the `clientAuthEnabled` property to `true`, you must also include a function that generates and passes a JWT token. The function must return a `Promise` that resolves to a signed JWT token string. The SDK will use this function to generate a new token whenever it needs to establish a new connection because the existing token has expired. The script would look something like this:

```js
// settings.js
var chatSettings = {
    URI: '<Server URI>',
    clientAuthEnabled: true
};

function generateToken() {
    return new Promise(function(resolve) {
        fetch('https://yourbackend.com/endpointToGenerateJWTToken')
            .then(function(token) {
               resolve(token);
            })
            .catch(function(error) {
                console.log('Token generation error:', error);
            });
    });
}

function initSDK(name) {
    // If WebSDK is not available, reattempt later
    if (!document || !WebSDK) {
        setTimeout(function() {
            initSDK(name);
        }, 2000);
        return;
    }

    // Default name is Bots
    if (!name) {
        name = 'Bots';
    }

    setTimeout(function() {
        var Bots = new WebSDK(chatSettings, generateToken);    // Initiate library with configuration

        var isFirstConnection = true;
        Bots.on(WebSDK.EVENT.WIDGET_OPENED, function() {
            if (isFirstConnection) {
                Bots.connect()                          // Connect to server
                    .then(function() {
                        console.log('Connection Successful');
                    })
                    .catch(function(reason) {
                        console.log('Connection failed');
                        console.log(reason);
                    });
                   isFirstConnection = false;
            }
        });

        window[name] = Bots;
    }, 0);
}
```

*Et voila!* You have an app integrated with Oracle Web SDK.

### Import the SDK Library in JavaScript

To import the library dynamically in JavaScript, use the following utility function, which is based on the [MDN example](https://developer.mozilla.org/en-US/docs/Web/API/HTMLScriptElement#Dynamically_importing_scripts) for importing scripts dynamically:

```js
function fetchSDK(src, onloadFunction, name) {
    var script = document.createElement('script');
    script.type = 'application/javascript';
    script.async = true;    // load the script asynchronously
    script.defer = true;    // fallback support for browsers that does not support async
    script.onload = function() {
        onloadFunction(name);
    };
    document.head.appendChild(script);
    script.src = src;
}

fetchSDK('<path of the web-sdk>', initSDK, '<WebSDK namespace>');
```

### Import the Library Using the Asynchronous Module Definition API

You can import the library using implementations of the Asynchronous Module Definition (AMD) API such as RequireJS with Oracle JET, and SystemJS.

```js
requirejs.config({
    paths: {
        WebSDK: '<path of the web-sdk>' // replace this with actual library path
    }
});

define(['WebSDK'], function(WebSDK) {
    var settings = {
        URI: '<Server URI>',
        channelId: '<Channel ID>',
        userId: '<User ID>'
    };
    Bots = new WebSDK(settings);

    Bots.connect();
});

```

## Browser Support
The SDK is supported on these browsers on Mac, Windows, and Linux:
* Firefox
* Chrome
* Safari
* Edge

For mobile platforms the following browsers are supported:
* Android browser
* iOS Safari

## SDK Security

The Web SDK can connect to the Oracle Digital Assistant web channel in two modes: client auth disabled and client auth enabled.

### Channel with Client Auth Disabled

When client authentication has been disabled, only connections made from unblocked lists (allowed domains) are allowed at the server. This use case is recommended when the client application can’t generate a signed JWT Token (because of a static website or no authentication mechanism for the web/mobile app) but requires ODA integration. It can also be used when the chat widget is already secured and visible to only authenticated users in the client platforms (Web Application with the protected page).

When connecting to such channels, `channelId` must be passed as a setting parameter during SDK initialization. The `userId` is also required to establish the connection. If you don't provide a value during initialization, then the SDK generates a random `userId`.

```js
{
    URI: 'oda-instance.com',
    channelId: '626f5db1-f99a-4984-86ee-df2d734537e6',
    userId: 'Jessica'
}
```

### Channel with Client Auth Enabled

In addition to unblocked lists, client authentication is enforced by signed JWT tokens.

The token generation and signing must be done by the client in the backend server ( preferably after user/client authentication) which is capable of maintaining the `keyId` and `keySecret` safe.

When the SDK needs to establish a connection with the ODA server, it first requests a JWT token from the client and then sends it along with the connection request. The ODA server validates the token signature and obtains the claim set from the JWT payload to verify the token to establish the connection.

To enable this mode, these two fields are required during SDK initialization: `clientAuthEnabled: true` must be passed in the SDK settings parameter, and a **token generator function** must be passed as the second parameter. The function must return a `Promise`, which is resolved to return a signed JWT token string.

```js
function generateToken() {
    return new Promise(function(resolve) {
        fetch('https://yourbackend.com/endpointToGenerateJWTToken').then(function(token) {
            resolve(token);
        });
    });
}

Bots.init({
    URI: 'oda-instance.com',
    clientAuthEnabled: true
}, generateToken);
```

### JWT Token

The JWT token generation and signing are the responsibility of the client application. Some token payload fields are mandatory and are validated by the ODA server.

Clients must use the HS256 signing algorithm to sign the tokens. The tokens must be signed by the secret key of the client auth enabled channel to which the connection is made. The body of the token must have the following claims:

* `iat` - issued at time - must be a number representing seconds since UNIX epoch
* `exp` - expiry time - must be a number representing seconds since UNIX epoch
* `channelId` - channel ID - must be a string
* `userId` - user ID - must be a string

Here's a sample signed JWT token:

Encoded token:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY3NDcyMDUsImV4cCI6MTU3Njc1MTExNywiY2hhbm5lbElkIjoiNDkyMDU5NWMtZWM3OS00NjE3LWFmOWYtNTk1MGQ2MDNmOGJiIiwidXNlcklkIjoiSm9obiIsImp0aSI6ImQzMjFjZDA2LTNhYTYtNGZlZS05NTBlLTYzZGNiNGVjODJhZCJ9.lwomlrI6XYR4nPQk0cIvyU_YMf4gYvfVpUiBjYihbUQ
```

Decoded token:

Header:

```json
{
    "typ": "JWT",
    "alg": "HS256"
}
```

Payload:

```json
{
    "iat": 1576747205,
    "exp": 1576748406,
    "channelId": "4920595c-ec79-4617-af9f-5950d603f8bb",
    "userId": "John"
}
```

> If any claim in the token is missing or has an incorrect format for its value, an error message is thrown by the SDK describing the cause, and the connection is not attempted. The error message can be used to fix the issue with the JWT token.

Any additional claims passed in the payload do not affect the client authentication mechanism.

## Settings

Use these properties to configure the chat widget:

### Network Configuration
| Property name | Optional | Default Value | Description |
| ------ | ------ | ------ | ------ |
| **`URI`** | No || The host name in Oracle Digital Assistant instance URL. Only the first path (`/`) needs to be passed here. You can pass this URL either with, or without, the protocol (`https://`).  |
| **`channelId`** | No || The Web Channel ID |
| **`userId`** | Yes | Random generated value | A unique identifier for the user. This ID gets initialized by SDK if one has not been provided. |
| **`clientAuthEnabled`** | Yes | `false` | Determines whether the SDK is connecting to a client authentication-enabled channel. This must be set to `true` to connect to such a channel and use a JWT token for authentication. |

### Feature Flags
| Property name | Default Value | Description |
| ------ | ------ | ------ |
| **`delegate`** || An object that enables you to set a delegate to receive callbacks before certain events in the conversation. See [Delegation](#delegation) for more details. |
| **`embedded`** | `false` | Embeds the chat widget inside another element referenced by `targetElement` setting. See [Embedded mode](#embedded-mode) for more details. |
| `targetElement` || The ID of the HTML element in DOM, such as a `div`, in which the chat widget is embedded. to embed the chat widget. Must be passed when `embedded` is set `true`. The element must have some size (height and width), as the widget takes the dimensions of this container. |
| **`enableAttachment`** | `true` | Enables the user to share files and location. |
| **`enableAttachmentSecurity`** | `false` | *Only applicable for client auth enabled connections to ODA platform Version 20.12 and above*. When set `true`, extra headers are passed to the attachment upload requests to ensure that they can't be downloaded without passing a valid signed JWT token in the URL as the value of `token` query parameter in the attachment fetch request URL. The setting must not be enabled if connecting to an ODA instance Version 20.08 or older for compatibility. |
| **`enableHeaderActionCollapse`** | `true` | Collapses the header actions into a menu button if the icon count is more than two. |
| **`shareMenuItems`** | `['audio', 'file', 'location', 'visual']` | The categories shown in the share popup menu. Accepts an array with string values mapped to menu items - `'visual'` for image and videos, `'audio'` for audio, `'file'` for files, and `'location'` for location. Only the categories for passed, correct values are shown in the menu. If no/all incorrect values are passed, all menu categories are shown. Also allows passing custom share items. See [Restrict attachment types](#restrict-attachment-types) for more details on the flag and passing custom menu items. |
| **`enableAutocomplete`** | `false` | Provides autocomplete suggestions as a user types a message in the input field. See [Autocomplete](#autocomplete) for more details. |
| **`enableAutocompleteClientCache`** | `false` | Enables client-side caching to minimize server calls when the user uses the autocomplete feature |
| **`enableBotAudioResponse`** | `false` | Enables the utterance of a skill's responses as they are received using the Web speech synthesis API. See [Response Narration](#response-narration) for more details. |
| **`enableDefaultClientResponse`** | `false` | When set to `true`, the client displays default responses when the skill response has been delayed, or when there's no response from the skill. See [Default Client Responses](#default-client-responses) for more details. |
| **`enableVoiceOnlyMode`** | `false` | Enables the voice-only mode. Activating the voice-only mode eliminates the need for users to click the mic button each time after they receive a bot message. With this mode enabled, the SDK automatically initiates voice recognition after the received message, with TTS (Text-to-Speech) it will initiate it after the message has been spoken out. |
| **`initBotAudioMuted`** | `true` | Initializes the skill message utterance in muted mode. Only applicable when `enableBotAudioResponse` is `true`. |
| **`disableInlineCSS`** | `false` | Enable to stop web-sdk from inserting inline css. Requires you to link the css file yourself in your webpage. |
| **`ttsVoice`** | | An array containing preferred voices used for speaking responses. Each item in the array should be an object with at least one of the following fields: `lang` and `name`. The first item that matches a voice that’s available in the system will be used for the TTS. |
| **`skillVoices`** | | `Deprecated` - An array containing preferred voices used for speaking out responses. Each item in the array should be an object with at least one of the following fields: `lang`, and `name`. The first item that matches a voice that’s available in the system will be used for the TTS. |
| **`ttsService`** | `oracle` | Injects a custom speech synthesis service that's used for uttering the skill responses. See [Speech Synthesis Service Injection](#speech-synthesis-service-injection) for more details. |
| **`enableHeadless`** | `false` | Initializes SDK instances without its chat widget while exposing its methods. Enables you to develop your own UI for the chat. See [Headless SDK](#headless-sdk) for more details. |
| **`enableLongPolling`** | `false` | Enables use of HTTP-based communication with the skill as a fallback if the WebSocket connection fails. See [Long Polling](#long-polling) for more details. |
| **`enableSpeech`** | `false` | Enables voice recognition service to allow the user to converse with the skill using voice messages by converting their voice input to a text message. See [Voice Recognition](#voice-recognition) for more details. |
| **`enableSpeechAutoSend`** | `true` | Automatically sends voice recognized text to the skill |
| **`speechLocale`** | `'en-us'` | The locale of the voice recognition the user is expected to speak in. The currently supported locales are available at section [WebSDK.SPEECH_LOCALE](#websdkspeech_locale). |
| **`enableTabsSync`** | `true` | Synchronizes conversation messages across different tabs for a given `userId` and `channelId`. See [Cross-Tab Conversation Synchronization](#cross-tab-conversation-synchronization) for more details. |
| **`timestampMode`** | `'relative'` | Enables the timestamp as either absolute timestamps that appear on each message when set `'absolute'`, or as a relative timestamp that appears only on the latest message, when set as `'relative'` or `'default'` and disables the timestamp if set to `'none'`. See [Relative Timestamps](#relative-timestamps) for more details. |
| **`timestampFormat`** | | Allows the formatting of the delivery timestamp shown with messages. Accepts values in the [DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat#Syntax) options object or a pattern string. See  [Format message timestamps](#format-message-timestamps) for more details. |
| **`timestampHeaderMode`** | `'absolute'` | Configures the timestamp headers that appear above the first message of the day. `'absolute'` displays the full timestamp in absolute format, `'relative'` displays it in a relative format, and `'none'` hides the timestamp header entirely. |
| **`timestampHeaderFormat`** | | Allows customization of the header timestamp format. Accepts values in the [DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat#Syntax) options object or a pattern string compatible with `timestampFormat`. |
| **`multiLangChat`** | | Adds a dropdown menu in the header that enables the user to select their preferred conversation language or defer to the skill to detect the user's language. See [Multi-Lingual Chat](#multi-lingual-chat) for more details. |
| **`webViewConfig`** | `{ referrerPolicy: 'no-referrer-when-downgrade', closeButtonType: 'icon', size: 'tall' }` | Enables customization to the in-widget webview, including its clear button, its header, and the partial or full-screen sizing of the webview itself. See [In-Widget Webview](#in-widget-webview) for more details. |

### Functionality Configuration
| Property name | Default Value | Description |
| ------ | ------ | ------ |
| **`alwaysShowSendButton`** | `false` | Displays the send button in the chat footer even when there's no user input text. |
| **`customHeaderElementId`** || The ID of the element to add to the chat widget header. Used for adding additional elements to the chat widget header. |
| **`disablePastActions`** | `'all'` | Disables action buttons in a skill message after the user has interacted with postback, location or form submit action. The allowed values are `all`, `none`, or `postback`. When set to `all`, all action buttons of the message and form input fields are disabled upon interaction. Setting `postback` only disables postback, location, form input fields and submit action. Setting `none` keeps all buttons enabled even after an interaction. |
| **`defaultGreetingTimeout`** | `5` | The default timeout, in seconds, after which a default greeting message displays. |
| **`defaultWaitMessageInterval`** | `5` | The default interval, in seconds, that the default wait message displays.|
| **`displayActionsAsPills`** | `false` | If set to `'true'`, display local actions along with global actions outside the message bubble |
| **`embeddedVideo`** | `true` | Embeds YouTube, Daily Motion, Vimeo, and Oracle Video Hub video links in messages when set to `'true'`. These videos are always embedded in the video attachment messages. |
| **`embedBottomScrollId`** || The ID of the element to be added as scrollable content at bottom of the chat. The element must be a part of the DOM. |
| **`embedBottomStickyId`** || The ID of the element to be added as pinned content at bottom of the chat. The element must be a part of the DOM. |
| **`embedTopScrollId`** || The ID of the element to be added as scrollable content at top of the chat. The element must be a part of the DOM. |
| **`embedTopStickyId`** || The ID of the element to be added as pinned content at top of the chat. The element must be a part of the DOM. |
| **`enableAgentSneakPreview`** | `false` | Sends the user-entered text along with typing status to the agent. |
| **`enableClearMessage`** | `false` | Displays a clear messages button in the chat widget header |
| **`enableDraggableButton`** | `false` | Enables the user to drag the launch button out of the way when it's blocking content on the page. See the [Draggable launch button and widget](#draggable-launch-button-and-widget) section for more details. |
| **`enableDraggableWidget`** | `false` | Enables the user to drag the chat widget out of the way when it's blocking content on the page. See the [Draggable launch button and widget](#draggable-launch-button-and-widget) section for more details. |
| **`enableEndConversation`** | `true` | Enables the user to end the conversation and reset the chat session. It also clears the local conversation history, disconnects from the chat server and minimizes the widget |
| **`enableLocalConversationHistory`** | `false` | Loads previous conversations for a passed userId on the current browser when the chat widget is initialized |
| **`enableResizableWidget`** | `false` | Enables the user to resize the chat widget after expanding it. If the widget is located on the right side of the web page, users can adjust its dimensions by dragging the top edge, left edge, or top-left corner. In the same way, if the widget is placed on the left side, users can resize the top edge, right edge, or top-right corner. |
| **`enableSendTypingStatus`** | `false` | Sends the typing status of the user to the live agent. |
| **`focusOnNewMessage`** | `'input'` | Sets the focus either on the user input field or the first action button in a message when a new message is received. When set to `'action'`, the focus is the first action button (if the message has action buttons) when a message is received. If the message has no buttons, then the focus is the user input field. When set to `'input'`, the user input field remains as the focus when new messages are received. See [Focus first action of skill message](#focus-first-action-of-skill-message) for more details. |
| **`hotkeys`** | `{}` | An object that contains a list of keyboard keys that activate, or focus, elements using the ALT Key combined with the passed hotkey. See [Keyboard Shortcuts - Hotkeys](#keyboard-shortcuts---hotkeys) for more details. |
| **`i18n`** | `{'en': {...}}` | The object that contains locale fields; each locale maintains `i18n` key-value pairs for certain strings that are used in the widget. See [Custom Text](#custom-text) for the strings that you can customize. |
| **`icons`** | `{}` | The object that can be used to pass custom icon resources to be displayed in place of default ones |
| **`initUserHiddenMessage`** || A user message to send once the chat widget is expanded and connected to the skill, without displaying the message in the chat widget. Used to initiate the conversation automatically. The message can be a text string, like `'Hi'`, or a message object, like `{ type: 'text', text: 'Hi'}`, or `{ messagePayload: { type: 'text', text: 'Hi'}}`. |
| **`initUserProfile`** || Initializes the user profile before the conversation starts. The profile payload must be of format `{ profile: {...} }`. The profile is updated before sending the value in `initUserHiddenMessage`. |
| **`initMessageOptions`** | `{ sendAt: 'expand' }` | Customizes the `initUserHiddenMessage` and `initUserProfile` behavior. It accepts an object with a `sendAt` property that can be set to either `'expand'` or `'init'`. If set `'expand'`, the init messages are sent once the chat widget is expanded. If set `'init'` on the other hand, the init messages are sent immediately on connection, whether the widget is expanded or not. |
| **`isDebugMode`** | `false` | Allows the SDK to log statements in the console for debugging purposes |
| **`linkHandler`** | `{ onclick: <function>, target: 'string' }` | An object that overrides the configuration for handling the clicks on the links that are embedded in the skill's responses. This object handles links in two ways, by setting the link's target in field `target` that accepts a string, and/or by adding a click event listener in the `onclick` field. When you want all links to open in the Webview, pass `linkHandler: { target: 'oda-chat-webview'}`. See [Open Links](#open-links) for more details. |
| **`locale`** | `'en'` | The default locale that is used for the informational text in the SDK. The passed locale value has a higher preference over users' browser locales. If there isn't an exact match, then the SDK attempts to match the closest language. For example, if the locale is `'da-dk'`, but `i18n` translations are provided only for `'da'`, then the `'da'` translation is used. In absence of translations for the passed locale, translations are searched and applied for browser locales. In absence of translations for any of them, the default locale, `'en'` is used for translations. |
| **`messageCacheSizeLimit`** | `2000` | Maximum number of messages to be saved in localStorage at a time |
| **`name`** | `'oda-chat'` | The name for the instance. Provides a namespace to the instance and is used as prefix for the CSS classnames and element IDs. |
| **`openChatOnLoad`** | `false` | Expands chat widget when the SDK instance is initialized |
| **`openLinksInNewWindow`** | `false` | If set to `true`, the target is opened in a new window when a link in a message is clicked. The browser's preference is not followed. See [Open Links](#open-links) for more details. |
| **`reconnectInterval`** | `5` | Time interval in seconds between a reconnection is attempted after a failure to connect to skill |
| **`reconnectMaxAttempts`** | `5` | The number of attempts made by the chat widget to reconnect when the initial connection fails. |
| **`showConnectionStatus`** | `false` | Displays current connection status in chat header below title |
| **`showPrevConvStatus`** | `true` | Displays a status message at the end of messages from previous conversations for given userId |
| **`showTypingIndicator`** | `true` | Displays an indicator in conversation pane while waiting for the skill's response |
| **`typingIndicatorTimeout`** | `30` | Allows setting the time, in seconds, after which the typing indicator is automatically removed if the chat widget has not yet received the response. |
| **`typingStatusInterval`** | `3` | Sets the interval, in seconds, to throttle the typing status that's sent to the live agent. |
| **`storageType`** | `'localStorage'` | A web storage mechanism that is used to store the conversation history of users whose `userId` is passed by the host app. The supported values are `'localStorage'` and `'sessionStorage'`. Anonymous users' conversations are always stored in `sessionStorage` and deleted automatically when the browser session ends. |
| **`theme`** | `'default'` | Chat widget theme. The supported values are `'default'`, a dark blue theme, `'redwood-dark`, a dark redwood theme, and `'classic'`, a light blue theme. |

### Layout Modification
| Property name | Default Value | Description |
| ------ | ------ | ------ |
| **`actionsLayout`** | `'vertical'` | Sets the layout direction for the local actions. When you set this as `'horizontal'`, these buttons are laid out horizontally and will wrap if the content overflows.|
| **`badgePosition`** | `{top: '0', right: '0'}` | The position of the notification badge icon with respect to the skill button |
| **`cardActionsLayout`** | `'vertical'` | Sets the layout direction for the card actions. When you set this as `'horizontal'`, these buttons are laid out horizontally and will wrap if the content overflows.
| **`formActionsLayout`** | `'vertical'` | Sets the layout direction for the form actions. When you set this as `'horizontal'`, these buttons are laid out horizontally and will wrap if the content overflows. |
| **`colors`** | `{branding: '#1B8FD2', text: '#212121', textLight: '#737373'}` | The colors used in the chat widget. See [Custom Colors](#custom-colors) for more details. |
| **`conversationBeginPosition`** | `'bottom'` | The starting position of the conversation in the widget. If set to `'top'`, the first messages appear on the top of the widget. If `'bottom'`, they appear on the bottom. |
| **`font`** | `'16px "Oracle Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue'` | The font style used for the widget wrapper. |
| **`fontFamily`** | `'"Oracle Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue"` | The font family used for all of the text in the chat widget. This setting takes precedence over the `font` configuration. |
| **`fontSize`** | `'16px'` | The font size to use for the header, bubble, and footer text in the widget. This setting takes precedence over the `font` configuration. |
| **`globalActionsLayout`** | `'vertical'` | Sets the layout direction for the global actions. When you set this as `'horizontal'`, these buttons are laid out horizontally and will wrap if the content overflows.
| **`height`** | `'620px'` | The height of the chat widget. Must be set to one of the [length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) values |
| **`messagePadding`** | `'6px 16px'` | Padding around messages in the chat widget |
| **`position`** | `{bottom: '20px', right: '20px'}` | A field to specify where to place the chat widget in the browser window. Must be passed as a JSON object |
| **`width`** | `'375px'` | The width of the chat widget. Must be set to one of the [length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) values |



### Custom Colors

You can modify the following colors to customize the look of the widget. The provided color must be a hexadecimal color. If you don't provide a color, then a default color is used instead.
The colors can be configured using the CSS variables defined on the chat wrapper (`.oda-chat-wrapper`) or by passing the `colors` configuration. We recommend using CSS variables.

| CSS Variable | Color Config Key | Description |
| ------ | ------ | ------ |
|`--color-branding` | `branding` | The primary color for branding the widget. The color is used as the header background, and as the hover color on footer buttons. |
|`--color-launch-icon-background` | `launchIconBackground` | The background color of the launch icon. |
|`--color-text` | `text` | The text color of the messages in the chat widget. It gets overridden if the component-specific setting is applied. |
|`--color-text-light` | `textLight` | The text color of the secondary text in messages, such as the card descriptions in the chat widget |
|`--color-header-background` | `headerBackground` | The background color of the chat widget's header |
|`--color-header-button-fill` | `headerButtonFill` | The SVG fill color of buttons in the chat header |
|`--color-header-text` | `headerText` | The color of title in the chat header |
|`--color-header-button-background-hover` | `headerButtonBackgroundHover` | The background color of the header buttons on hover |
|`--color-header-button-fill-hover` | `headerButtonFillHover` | The fill color of the header buttons on hover |
|`--color-conversation-background` | `conversationBackground` | The background of the chat widget's conversation pane. It accepts all values supported by the `background` [CSS property](https://developer.mozilla.org/en-US/docs/Web/CSS/background), so it can also be used to set image backgrounds, gradients, etc. |
|`--color-bot-message-background` | `botMessageBackground` | The skill message background color |
|`--color-bot-text` | `botText` | The skill text color. Overrides the `text` color, if passed. |
|`--color-user-message-background` | `userMessageBackground` | The user message background color |
|`--color-user-text` | `userText` | The user text color. Overrides the `text` color, if passed. |
|`--color-actions-background` | `actionsBackground` | The action button background color |
|`--color-actions-background-focus` | `actionsBackgroundFocus` | The action button background color on focus |
|`--color-actions-background-hover` | `actionsBackgroundHover` | The action button background color on hover |
|`--color-actions-border` | `actionsBorder` | The action button border color |
|`--color-actions-text` | `actionsText` | The action button text color |
|`--color-actions-text-focus` | `actionsTextFocus` | The action button text color on focus |
|`--color-actions-text-hover` | `actionsTextHover` | The action button text color on hover |
|`--color-global-actions-background` | `globalActionsBackground` | The global action button background color |
|`--color-global-actions-background-focus` | `globalActionsBackgroundFocus` | The global action button background color on focus |
|`--color-global-actions-background-hover` | `globalActionsBackgroundHover` | The global action button background color on hover |
|`--color-global-actions-border` | `globalActionsBorder` | The global action button border color |
|`--color-global-actions-text` | `globalActionsText` | The global action button text color |
|`--color-global-actions-text-focus` | `globalActionsTextFocus` | The global action button text color on focus |
|`--color-global-actions-text-hover` | `globalActionsTextHover` | The global action button text color on hover |
|`--color-primary-actions-background` | `primaryActionsBackground` | The primary action button background color |
|`--color-primary-actions-background-focus` | `primaryActionsBackgroundFocus` | The primary action button background color on focus |
|`--color-primary-actions-background-hover` | `primaryActionsBackgroundHover` | The primary action button background color on hover |
|`--color-primary-actions-border` | `primaryActionsBorder` | The primary action button border color |
|`--color-primary-actions-text` | `primaryActionsText` | The primary action button text color |
|`--color-primary-actions-text-focus` | `primaryActionsTextFocus` | The primary action button text color on focus |
|`--color-primary-actions-text-hover` | `primaryActionsTextHover` | The primary action button text color on hover |
|`--color-danger-actions-background` | `dangerActionsBackground` | The danger action button background color |
|`--color-danger-actions-background-focus` | `dangerActionsBackgroundFocus` | The danger action button background color on focus |
|`--color-danger-actions-background-hover` | `dangerActionsBackgroundHover` | The danger action button background color on hover |
|`--color-danger-actions-border` | `dangerActionsBorder` | The danger action button border color |
|`--color-danger-actions-text` | `dangerActionsText` | The danger action button text color |
|`--color-danger-actions-text-focus` | `dangerActionsTextFocus` | The danger action button text color on focus |
|`--color-danger-actions-text-hover` | `dangerActionsTextHover` | The danger action button text color on hover |
|`--color-card-background` | `cardBackground` | The card message's background color |
|`--color-card-nav-button` | `cardNavButton` | The card navigation button background color |
|`--color-card-nav-button-focus` | `cardNavButtonFocus` | The card navigation button background color on focus |
|`--color-card-nav-button-hover` | `cardNavButtonHover` | The card navigation button background color on hover |
|`--color-rating-star` | `ratingStar` | The color that's applied to rating stars of the feedback message in their initial unselected state. |
|`--color-rating-star-fill` | `ratingStarFill` | The color that's applied to rating stars of feedback message on hover or selection. The `branding` color is used if this is not passed. |
|`--color-links` | `links` | The color of the links that are embedded in skill messages. |
|`--color-user-links` | `userLinks` | The color of the links that are embedded in user messages. |
|`--color-horizontal-rule-background` | `horizontalRuleBackground` | The color of the separator that's displayed at the end of the previous conversation |
|`--color-timestamp` | `timestamp` | The color of the timestamp header and the relative timestamp in messages |
|`--color-agent-initials` | `agentInitials` | The color of the agent initials that is displayed alongside the agent messages |
|`--color-agent-avatar-background` | `agentAvatarBackground` | The background color of the agent initials avatar that is displayed alongside the agent messages |
|`--color-agent-name` | `agentName` | The color of the agent name that is displayed above the agent messages |
|`--color-typing-indicator` | `typingIndicator` | The background fill color of the typing indicator |
|`--color-footer-background` | `footerBackground` | The background color of the chat widget's footer |
|`--color-footer-button-fill` | `footerButtonFill` | The SVG fill color of the buttons in chat footer |
|`--color-footer-button-background-hover` | `footerButtonBackgroundHover` | The background color of the footer buttons on hover |
|`--color-footer-button-fill-hover` | `footerButtonFillHover` | The SVG fill color of the footer buttons on hover |
|`--color-input-background` | `inputBackground` | The background color of the message input field |
|`--color-input-border` | `inputBorder` | The border color of the input field |
|`--color-input-text` | `inputText` | The text color in the message input field. Overrides `text`, if passed. |
| -- | `shareMenuText` | The text color used by the share menu items. Overrides `text`, if passed. [ `Deprecated` - Use `--color-popup-button-text` instead ] |
| -- | `recognitionViewBackground` | The background color of the recognition text view that is displayed in voice mode. If this color is absent, the header background color is used. [ `Deprecated` - Not required anymore based on the design upgrade ]|
|`--color-recognition-view-text` | `recognitionViewText` | The text color in the recognition text view that is displayed in voice mode. If it's absent, text color is used. |
| -- | `recognitionViewButtonFill` | The SVG fill color of the mode toggle color in voice mode |
|`--color-visualizer-container-background` | `visualizerContainerBackground` | The background color of the visualizer container displayed in voice mode. If absent, the user message background color is used. |
|`--color-visualizer` | `visualizer` | The color used in the bars of the visualizer graph. If it's absent, the branding color is used instead. |
|`--color-notification-badge-background` | `notificationBadgeBackground` | The background color of the message notification badge |
|`--color-notification-badge-text` | `notificationBadgeText` | The text color of message count in notification badge |
|`--color-popup-background` | `popupBackground` | The background color of prompts and popups |
|`--color-popup-text` | `popupText` | The text and icon color of prompts and popups |
|`--color-popup-button-background` | `popupButtonBackground` | The background color of popup buttons |
|`--color-popup-button-text` | `popupButtonText` | The text color of popup buttons |
|`--color-popup-horizontal-rule` | `popupHorizontalRule` | The horizontal rule color for separator for multi-lang chat menu action |
|`--color-popup-item-background-hover` | `popupItemBackgroundHover` | The background color on hover of popup list items |
|`--color-table-header-background` | `tableHeaderBackground` | The background color of table headers |
|`--color-table-header-text` | `tableHeaderText` | The text color of table headers |
|`--color-table-background` | `tableBackground` | The background color of tables |
|`--color-table-text` | `tableText` | The text color of tables |
|`--color-table-separator` | `tableSeparator` | The separator color of table rows |
|`--color-table-row-background-hover` | `tableRowBackgroundHover` | The background color of table rows on hover in table-form messages |
|`--color-table-actions-background` | `tableActionsBackground` | The background color of table actions |
|`--color-table-actions-background-focus` | `tableActionsBackgroundFocus` | The background color of table actions on focus |
|`--color-table-actions-background-hover` | `tableActionsBackgroundHover` | The background color of table actions on hover |
|`--color-table-actions-border` | `tableActionsBorder` | The border color of table actions |
|`--color-table-actions-text` | `tableActionsText` | The text color of table actions |
|`--color-table-actions-text-focus` | `tableActionsTextFocus` | The text color of table actions on focus |
|`--color-table-actions-text-hover` | `tableActionsTextHover` | The text color of table actions on hover |
|`--color-form-header-background` | `formHeaderBackground` | The background color of form titles |
|`--color-form-header-text` | `formHeaderText` | The text color of form titles |
|`--color-form-background` | `formBackground` | The background color of forms |
|`--color-form-text` | `formText` | The text color of forms |
|`--color-form-input-background` | `formInputBackground` | The background color of the input fields in Edit-Form messages |
|`--color-form-input-border` | `formInputBorder` | The border color of the input fields in Edit-Form messages |
|`--color-form-input-border-focus` | `formInputBorderFocus` | The border color of the input fields on focus in Edit-Form messages |
|`--color-form-input-text` | `formInputText` | The text color of the input fields in Edit-Form messages |
|`--color-form-label` | `formLabel` | The color of the form labels |
|`--color-form-error` | `formError` | The SVG fill color of the icon in field-level and form-level error messages that is displayed in Edit-Form messages. The color is used as the border color of input field upon error in Edit-Form messages. |
|`--color-form-error-text` | `formErrorText` | The text color of field-level error message that is displayed in Edit-Form messages |
|`--color-form-actions-background` | `formActionsBackground` | The background color of form actions |
|`--color-form-actions-background-focus` | `formActionsBackgroundFocus` | The background color of form actions on focus |
|`--color-form-actions-background-hover` | `formActionsBackgroundHover` | The background color of form actions on hover |
|`--color-form-actions-border` | `formActionsBorder` | The border color of form actions |
|`--color-form-actions-text` | `formActionsText` | The text color of form actions |
|`--color-form-actions-text-focus` | `formActionsTextFocus` | The text color of form actions on focus |
|`--color-form-actions-text-hover` | `formActionsTextHover` | The text color of form actions on hover |
|`--color-primary-form-actions-background` | `primaryFormActionsBackground` | The background color of primary actions in Table, Form, Table-Form and Edit-Form messages |
|`--color-primary-form-actions-background-focus` | `primaryFormActionsBackgroundFocus` | The background color of primary actions on focus in Table, Form, Table-Form and Edit-Form messages |
|`--color-primary-form-actions-background-hover` | `primaryFormActionsBackgroundHover` | The background color of primary actions on hover in Table, Form, Table-Form and Edit-Form messages |
|`--color-primary-form-actions-border` | `primaryFormActionsBorder` | The border color of primary actions in Table, Form, Table-Form and Edit-Form messages |
|`--color-primary-form-actions-text` | `primaryFormActionsText` | The text color of primary actions in Table, Form, Table-Form and Edit-Form messages |
|`--color-primary-form-actions-text-focus` | `primaryFormActionsTextFocus` | The background color of primary actions on focus in Table, Form, Table-Form and Edit-Form messages |
|`--color-primary-form-actions-text-hover` | `primaryFormActionsTextHover` | The background color of primary actions on hover in Table, Form, Table-Form and Edit-Form messages |
|`--color-danger-form-actions-background` | `dangerFormActionsBackground` | The background color of danger actions in Table, Form, Table-Form and Edit-Form messages |
|`--color-danger-form-actions-background-focus` | `dangerFormActionsBackgroundFocus` | The background color of danger actions on focus in Table, Form, Table-Form and Edit-Form messages |
|`--color-danger-form-actions-background-hover` | `dangerFormActionsBackgroundHover` | The background color of danger actions on hover in Table, Form, Table-Form and Edit-Form messages |
|`--color-danger-form-actions-border` | `dangerFormActionsBorder` | The border color of danger actions in Table, Form, Table-Form and Edit-Form messages |
|`--color-danger-form-actions-text` | `dangerFormActionsText` | The text color of danger actions in Table, Form, Table-Form and Edit-Form messages |
|`--color-danger-form-actions-text-focus` | `dangerFormActionsTextFocus` | The text color of danger actions on focus in Table, Form, Table-Form and Edit-Form messages |
|`--color-danger-form-actions-text-hover` | `dangerFormActionsTextHover` | The text color of danger actions on hover in Table, Form, Table-Form and Edit-Form messages |
|`--color-error-message-background` | `errorMessageBackground` | The background color of an error message bubble. The color is used as the background color of form-level error message that is displayed in Edit-Form messages. |
|`--color-error-border` | `errorBorder` | The border color of an error message bubble. The color is used as the border color of form-level error message that is displayed in Edit-Form messages. |
|`--color-error-title` | `errorTitle` | The title color of an error message content. The color is used as error text color of form-level error message that is displayed in Edit-Form messages. |
|`--color-error-text` | `errorText` | The description color of an error message content. |

Here's an example of providing a custom colors using css variables.
```css
.oda-chat-wrapper {
    --color-branding: '#e00';
    --color-text: '#545454';
}
```

Here's an example of providing a custom color using `colors` config.
```js
colors: {
    branding: '#e00',
    text: '#545454'
}
```
The branding and text color will be modified in the above example. The default color is used for secondary text color.

### Custom Icons

The icons used in the widget can be customized in two ways - the URL of the image asset, or an SVG string. For the icons that support SVG strings, you can pass the raw SVG data that the widget renders as an inline SVG. SVG strings allow for the faster loading of an image, the ability to animate it, or for changing its color. The theme color is applied to SVG strings for attachment, send, and mic buttons, but not other image assets.

Starting with 21.10, the SDK exposes `icons` property in settings to group all custom icons in a single configuration field.
All fields within the icons object support both image resource paths and raw SVG strings.
```js
var settings = {
    // ...,
    icons: {
        rating: '<svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" viewBox="0 0 24 24"><path d="M15.994 3.006a5.7 5.7 0 00-3.795 1.707L12 4.916l-.199-.202a5.676 5.676 0 00-8.128 0c-2.231 2.275-2.231 5.953 0 8.228L12 21.428l8.326-8.486A5.873 5.873 0 0022 8.828a5.873 5.873 0 00-1.675-4.115A5.693 5.693 0 0016.262 3z"/></svg>'
    }
};
```

Here's an example of how you provided custom icons in prior releases:
```js
var chatSettings = {
    ...,
    clearMessageIcon: 'https://cdn4.iconfinder.com/data/icons/kids-2/128/kids_kid_boy-32.png',
    micIcon: '<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none" opacity=".1"/><path d="M12 1c-4.97 0-9 4.03-9 9v7c0 1.66 1.34 3 3 3h3v-8H5v-2c0-3.87 3.13-7 7-7s7 3.13 7 7v2h-4v8h4v1h-7v2h6c1.66 0 3-1.34 3-3V10c0-4.97-4.03-9-9-9z"/></svg>'
};
```

| Property Name -- 21.10 Release | Property Name -- Prior Releases | Description |
| ------ | ------ | ------ |
| `avatarAgent` | `agentAvatar` | The avatar icon that's displayed alongside response messages from a live agent. If it is not set, but `avatarBot` is set, the `avatarBot` icon is displayed instead. If neither is provided, then no icon is displayed for response messages. |
| `avatarBot` | `botIcon` | The avatar icon that's displayed alongside response messages. No default avatar is displayed if this is not provided. |
| `avatarUser` | `personIcon` | The avatar icon that's displayed alongside user messages. No default avatar is displayed if this is not provided. |
| `fileAudio` | `audioIcon` | The icon in audio attachment messages when the audio URL is unreachable |
| `fileImage` | `imageIcon` | The icon in image attachment messages when the image URL is unreachable |
| `fileGeneric` | `fileIcon` | The icon in file attachment messages |
| `fileVideo` | `videoIcon` | The icon in video attachment messages when the video URL is unreachable |
| `clearHistory` | `clearMessageIcon` | The icon for chat header button to clear local conversation history |
| `close` |  | The icon that's displayed in close button in error message banners, expanded image previews, and the in-widget Webview. |
| `collapse` | `closeIcon` | The icon for chat header button to collapse the chat widget to launch button |
| `download` | `downloadIcon` | The icon for the button in image attachment messages to download the file |
| `error` | `errorIcon`  | The icon displayed alongside error messages like upload failure |
| `expandImage` | `expandImageIcon` | The icon for the button to expand the image in attachment messages to full-screen |
| `externalLink` |  | The icon to indicate that the link will take you to an external website |
| `keyboard` | `keyboardIcon` | The icon for chat footer button, displayed during voice recognition, to switch back to the text-based message input |
| `logo` | `logoIcon` | The logo icon displayed in chat header |
| `launch` | `botButtonIcon` | The icon for the button that's displayed during the collapsed state of the chat widget to launch the expanded widget |
| `mic` | `micIcon` | The icon used for the button in the chat footer used for switching to voice input mode and initiate voice recognition. |
| `rating` |  | The icon displayed for the feedback action buttons in the feedback rating component. For the best user experience for the hover action, pass a filled SVG icon string. |
| `send` | `sendIcon` | The icon for chat footer button to send messages |
| `shareMenu` | `attachmentIcon` | The icon for share menu button in chat footer |
| `shareMenuAudio` |  | The icon for the audio menu item in the share menu popup |
| `shareMenuFile` |  | The icon for the File menu item in the share menu popup |
| `shareMenuLocation` |  | The icon for the location menu item in the share menu popup |
| `shareMenuVisual` |  | The icon for the image/video menu item in the share menu popup |
| `ttsOff` | `audioResponseOffIcon` | The icon for chat header button to toggle message audio response when it is muted |
| `ttsOn` | `audioResponseOnIcon` | The icon for chat header button to toggle message audio response when it is on unmute |
| `typingIndicator` | `chatBubbleIcon` | The animated icon in conversation pane indicating a response being built from skill |

The following properties continued to be supported for compatibility, but their counterparts in `icons` property bag will be given preference.

| Property name | Description |
| ------ | ------ |
| `botButtonIcon` | The chat bot button that's displayed as the minimized chat button |
| `logoIcon` | The chat logo icon that's displayed at the header of the chat widget |
| `agentAvatar` | The Avatar icon that's displayed alongside the response messages coming from a live agent. If not provided, and `botIcon` is provided, then the `botIcon` is displayed. If neither `agentAvatar` nor `botIcon` is provided, then no icon is displayed. |
| `botIcon` | the icon alongside skill response messages. If not provided, no icon is displayed. |
| `personIcon` | The icon that displays alongside user messages. If not provided, no icon is displayed |
| `chatBubbleIcon` | The loading chat bubble icon |
| `clearMessageIcon` | The clear message button icon at widget header |
| `audioResponseOffIcon` | The icon of toggle button when audio responses are turned off |
| `audioResponseOnIcon` | The icon of toggle button when audio responses are turned on |
| `closeIcon` | The icon for the button to minimize chat widget at widget header |
| `attachmentIcon` | The attachment upload button icon |
| `sendIcon` | The send message button icon |
| `keyboardIcon` | The keyboard icon, displayed in button to switch from voice to keyboard mode |
| `micIcon` | The mic icon, displayed in button to switch from keyboard to voice mode |
| `audioIcon` | The audio attachment icon, displayed when attachment source URL is not reachable |
| `fileIcon` | The file attachment icon |
| `imageIcon` | The image attachment icon, displayed when attachment source URL is not reachable |
| `videoIcon` | The video attachment icon, displayed when attachment source URL is not reachable |
| `errorIcon` | The error icon. Displayed with error messages or information |
| `downloadIcon` | The icon for download button for skill attachment messages |
| `expandImageIcon` | The icon for image expand button for image attachments |

You can also resize the icon for the loading chat bubble icon (enabled with `chatBubbleIcon`).
| Property Name | Default Value | Description|Required?|
| ------ | ------ | ------ | ------ |
| `chatBubbleIconHeight` || The height of the loading chat bubble icon. |No|
| `chatBubbleIconWidth` || The width of the loading chat bubble icon |No|

### Custom Text
The following strings can be customized to provide localized text. The strings must be provided under a valid [language string](https://www.science.co.il/language/Locale-codes.php). For example: `'en-us'`, `'es'`, `'fr'`, `'zh-cn'`.

| Key | Default Value | Description |
| ------ | ------ | ------ |
| `agent` | `'Agent'` | The text used for the Agent. |
| `agentMessage` | `'{0} says'` | The skill message indicator for screen readers. It is spoken by the screen readers before the skill responses. The text (`{0}`) is replaced by the agent name. |
| `attachment_audio` | `'Audio attachment'` | The text used for the TTS utterance of an audio attachment. |
| `attachment_file` | `'File attachment'` | The text used for the TTS utterance of a file attachment. |
| `attachment_image` | `'Image attachment'` | The text used for the TTS utterance of an image attachment. |
| `attachment_video` | `'Video attachment'` | The text used for the TTS utterance of a video attachment. |
| `attachmentAudioFallback` | `'Your browser does not support embedded audio. However you can {0}download it{/0}.'` | The fallback message that is displayed in place of an audio attachment if the audio can not be rendered by the client. The text between `{0}` and `{/0}` is set to a link to download the file. |
| `attachmentVideoFallback` | `'Your browser does not support embedded video. However you can {0}download it{/0}.'` | The fallback message that's displayed in place of a video attachment if the video can not be rendered by the client. The text between `{0}` and `{/0}` is set to a link to download the file. |
| `audioResponseOff` | `'Turn audio response on'` | The tooltip that appears when hovering over the audio utterance on the button in the header. |
| `audioResponseOn` | `'Turn audio response off'` | The tooltip that appears when hovering over the audio utterance off the button in the header. |
| `avatarAgent` | `'Agent icon'` | The alternative text used for the agent icon that's displayed alongside the agent messages. |
| `avatarBot` | `'Bot icon'` | The alternative text used for the skill icon that's displayed alongside the skill messages. |
| `avatarUser` | `'User icon'` | The alternative text used for the user icon that's displayed alongside the user messages. |
| `card` | `'Card {0}'` | The card identifier. The text (`{0}`) is replaced by the card index. |
| `cardImagePlaceholder` | `'Card image'` | The text placeholder that's displayed while the card image is fetched and loaded. |
| `cardNavNext` | `'Next card'` | The card navigation button label that displays the next card in horizontal layout. |
| `cardNavPrevious` | `'Previous card'` | The card navigation button label that displays the previous card in horizontal layout. |
| `chatButtonTitle` || The title of the chat widget launch button. The `chatTitle` string is used if this is not passed.  |
| `chatTitle` | `'Chat'` | Title of the chat widget that is displayed on the header.  |
| `chatSubtitle` || The subtitle of the chat widget that's displayed on the header below the title. If `showConnectionStatus` is set to `true`, and the subtitle is set as well, then the subtitle displays in place of the connection status. |
| `clear` | `'Clear conversation'` | The tooltip that appears when hovering over the clear messages button in the header. |
| `close` | `'Close widget'` | The tooltip that appears when hovering over the close widget button in the header. |
| `closing` | `'Closing'` | The status text when the connection between the chat widget and the server is closing. |
| `connected` | `'Connected'` | The status text when the connection between the chat widget and the server is established. |
| `connecting` | `'Connecting'` | The status text when the connection between the chat widget and the server is connecting. |
| `connectionFailureMessage` | `'Sorry, the assistant is unavailable right now. If the issue persists, contact your help desk.'` | The failure message that displays when the widget can't connect to skill. |
| `connectionRetryLabel` | `'Try Again'` | The label of the retry connection button. |
| `defaultGreetingMessage` |  `'Hey, Nice to meet you! Allow me a moment to get back to you.'` | The default client greeting response that's displayed when the skill response has not been received within the number of seconds set by `defaultGreetingTimeout`. |
| `defaultWaitMessage` | `'I\'m still working on your request. Thank you for your patience!'` | The default response that displays at the interval when an actual skill response has not been received. This interval is set, in seconds, by `defaultWaitMessageInterval`. |
| `defaultSorryMessage`:  |`'I\'m sorry. I can\'t get you the right content. Please try again.'` | The default client response when  the skill response has not received within the number of seconds set by `typingIndicatorTimeout`.
| `disconnected` | `'Disconnected'` | The status text when the connection between the chat widget and the server is closed. |
| `download` | `'Download'` | The tooltip that appears when hovering over the download button in attachments. |
| `editFieldErrorMessage` | `'Field input is invalid'` | The field-level error message that is displayed in the Edit-Form messages when the value entered by the user is invalid for that field. SDK defaults to this message in-case `clientErrorMessage` is not supplied by the skill or browser validation errors are not present for input field. |
| `editFormErrorMessage` | `'Some of the fields need your attention'` | The form-level error message that is displayed below the form submit action in Edit-Form messages on client-side validation. This is shown when at least one of the fields is not valid and there are more than one field. SDK defaults to this message in-case `errorMessage` is not supplied by the skill in the message payload. |
| `endConversation` | `'End Conversation'` | The tooltip that appears when hovering over the end conversation header button. |
| `endConversationConfirmMessage` | `'Are you sure you want to end the conversation?'` | The confirmation message that displays when a user clicks the end conversation button. |
| `endConversationDescription` | `'This will also clear your conversation history.'` | The description message that displays along with the confirm message in the end conversation prompt. |
| `errorSpeechInvalidUrl` | `'ODA URL for connection is not set. Please pass \'URI\' parameter during SDK initialization.'` | The error message that is displayed when the voice server URL is invalid or not set. |
| `errorSpeechMultipleConnection` | `'Another voice recognition is ongoing. Can\'t start a new one.'` | The error message that's displayed when the user attempts a new voice message while another recognition is ongoing. This usually happens when multiple voice connections are attempted in a short interval by repeatedly toggling between keyboard and voice mode. |
| `errorSpeechTooMuchTimeout` | `'The voice message is too long to recognize and generate text.'` | The error message that's displayed when the user provides a voice message that can't be recognized because it's too long. |
| `errorSpeechUnavailable` | `'To allow voice messaging, update your browser settings to enable access to your microphone.'` | The error message that's displayed when the browser does not provide any API to access the microphone. |
| `errorSpeechUnsupportedLocale` | `'The locale set for voice recognition is not supported. Please use a valid locale in \'speechLocale\' setting.'` | The error message that's displayed when an unsupported speech locale is configured for voice recognition and a recording is attempted. |
| `inputPlaceholder` | `'Type a message'` | The placeholder text that appears in the user input field in keyboard mode. |
| `imageViewerClose` | `'Close image viewer'` | Accessibility text for the button that closes the expanded image. |
| `imageViewerOpen` | `'Open image viewer'` | Accessibility text for the button that expands the image. |
| `itemIterator` | `'Item {0}'` | Item identifier in a list of items in a message like Table, Form, or Table-Form message. The placeholder `{0}` is replaced by the item index. |
| `noResultText` | `'No more results'` | The status text that's displayed when there are no matches while doing a search in multi select dropdown list. |
| `noSpeechTimeout` | `'The voice could not be detected to perform recognition.'` | The status text that's displayed when the server is unable to recognize the voice. |
| `languageSelectDropdown` | `'Select chat language'` | The tooltip that appears when users hover over the language selection button in the header. |
| `language_detect` | `'Detect Language'` | The label for auto-detect option in language selection dropdown. |
| `language_<languageTag>` | *`Language Label`* | The label for the language represented by the `languageTag`. For example, `'English'` for `'en'` in the language selection dropdown available when  [Multi-Lingual Chat](#multi-lingual-chat) is configured. |
| `linkField` | `'Click on the highlighted text to open Link for {0}'` | The replacement utterance text for a link [Field](#field). The placeholder `{0}` is replaced with the `linkLabel` of the field. |
| `noText` | `'No'` | The label for the No confirmation button. |
| `openMap` | `'Open Map'` | The label of the action button to open a location map. |
| `previousChats` | `'End of previous conversation'` | The status text that's displayed at the end of older messages. |
| `ratingStar` | `'Rate {0} star'` | The tooltip text that's displayed for each rating star in a feedback message. The placeholder `{0}` is replaced by the number of stars that the user has selected. |
| `recognitionTextPlaceholder` | `'Speak your message'` | Placeholder text that appears in the recognition text field in voice mode. |
| `requestLocation` | `'Requesting location'` | Text that is displayed while user location is requested on the browser. |
| `requestLocationDeniedPermission` | `'To allow sharing your location, update your browser settings to enable access to your location. You can also type in the location instead.'` | The error message that's displayed when permission to access the location is denied. |
| `requestLocationDeniedTimeout` | `'It is taking too long to get your location. Please try sharing it again, or else type it in.'` | The error message that's displayed when the location request is not resolved due to a timeout. |
| `requestLocationDeniedUnavailable` | `'Your current location is unavailable. Please try sharing it again, or else type it in.'` | The error message that is displayed when the location request is denied due to the unavailability of the current location in the client's device. |
| `retryMessage` | `'Try again'` | Text that is displayed when a user message is not sent to the server. |
| `send` | `'Send message'` | Tooltip that appears when hovering over send button in the footer. |
| `shareAudio` | `'Share Audio'` | The menu item text for sharing an audio file in the share popup. |
| `shareFile` | `'Share File'` | The menu item text for sharing a generic file in the share popup. |
| `shareLocation` | `'Share Location'` | The menu item text for sharing a location in the share popup. |
| `shareVisual` | `'Share Image/Video'` | The menu item text for sharing an image or video file in the share popup. |
| `shareFailureMessage` | `'Sorry, sharing is not available on this device.'` | The error message that's shown when a user clicks on a share action button and the share API is not supported by the device. |
| `skillMessage` | `'Skill says'` | The skill message indicator for screen readers. It is spoken by the screen readers before the skill responses. |
| `showOptions` | `'Show Options'` | The tooltip that appears when users hover over the menu button in the header when the header actions are collapsed. |
| `speak` | `'Speak a message'` | The tooltip that appears when hovering over speak button in the footer. |
| `relTimeNow` | `'Now'`| The relative timestamp that's shown right after a new message |
| `relTimeMoment` | `'A few seconds ago'`| The relative timestamp that displays ten seconds after the message has been received and before 60 seconds has elapsed since the last message was received. |
| `relTimeMin` | `'{0}min ago'`| The relative timestamp that's shown for every minute since the last message. The placeholder `{0}` is replaced by the number of minutes passed. |
| `relTimeHr` | `'{0}hr ago'`| The relative timestamp shown for each hour since the last message. The placeholder `{0}` is replaced by the number of hours passed. |
| `relTimeDay` | `'{0}d ago'`| The relative timestamp that's shown each day since the last message. The placeholder `{0}` is replaced by the number of days passed. |
| `relTimeMon` | `'{0}mth ago'`| The relative timestamp shown for each month since the last message. The placeholder `{0}` is replaced by the number of months passed. |
| `relTimeYr` | `'{0}yr ago'`| The relative timestamp shown for every year since the last message. The placeholder `{0}` is replaced by the number of years passed. |
| `typingIndicator` | `'Waiting for response'` | The accessibility text for the typing indicator. It is spoken by the screen readers. |
| `upload` | `'Share popup'` | The tooltip that appears when hovering over the upload share popup button in the footer. |
| `uploadFailed` | `'Upload Failed.'` | The error text for an upload failure. |
| `uploadFileNetworkFailure` | `'Upload not completed due to network failure.'` | The error text that's displayed when the upload file does not complete due to network failure. |
| `uploadFileSizeLimitExceeded` | `'File size should not be more than {0}MB.'` | The error text that's displayed when the upload file size is too large. The placeholder `{0}` is replaced by the SDK to the maximum allowed file size, which defaults to 25MB. |
| `uploadFileSizeZeroByte` | `'Files of size zero bytes can\'t be uploaded.'` | The error text that's displayed when the upload file size is 0 bytes. |
| `uploadUnauthorized` | `'Upload request is unauthorized.'` | The error text that's displayed when the upload request is unauthorized. |
| `uploadUnsupportedFileType` | `'Unsupported file type.'` | The error text that's displayed when an unsupported file type upload is attempted. |
| `userMessage` | `'I say'` | The user message indicator for screen readers. It is spoken by the screen readers before the user messages. |
| `utteranceGeneric` | `'Message from skill.'` | The fallback description of a response message for an utterance that was not parsed by the SDK. |
| `webViewAccessibilityTitle` | `'In-widget Webview to display links'` | The default accessibility title for the Webview that is read out by screen readers |
| `webViewClose` | `'Done'` | The default label/tooltip title for Webview close button |
| `webViewErrorInfoDismiss` | `'Dismiss'` | The tooltip for the dismiss button that's used to close the fallback link inside the webview. |
| `webViewErrorInfoText` | `'Don’t see the page? {0}Click here{/0} to open it in a browser.'` | The informational text displayed in the webview when the clicked link can't be opened within it. The text between `{0}` and `{/0}` is set to the original link that opens in a new tab or window. |
| `yesText` | `'Yes'` | The label for the Yes confirmation button. |

Here's an example of providing custom text in a few locales.
```js
i18n: {
    fr: {
        chatTitle: 'Soutien'
    },
    en: {
        chatTitle: 'Support'
    },
    es: {
        chatTitle: 'Apoyo'
    },
    'zh-cn': {
        chatTitle: '支持'
    }
}
```
If custom strings are provided for any locale other than `en`, then all keys must be specified for that locale. Otherwise, `en` translations are displayed for the missing values.

The settings can be configured as provided in the example below:
```html
<script>
var chatSettings = {
    URI: '<Chat server URI>',
    channelId: '<Channel ID>',
    userId: '<User ID>',
    fontFamily: '"Helvetica Neue", Helvetica, Arial, sans-serif',
    locale: 'en',
    enableClearMessage: true,
    icons: {
        launch: 'style/Robot.png',
        avatarBot: 'style/Robot.png',
        avatarUser: 'style/userIcon.png'
    }
};

function initSDK(name) {
    // If WebSDK is not available, reattempt later
    if (!document || !WebSDK) {
        setTimeout(function() {
            initSDK(name);
        }, 2000);
        return;
    }

    // Default name is Bots
    if (!name) {
        name = 'Bots';
    }

    setTimeout(function() {
        var Bots = new WebSDK(chatSettings);    // Initiate library with configuration

        // Add ready listener before calling connect()
        // It is preferable to add other listeners before calling connect() too
        Bots.on('ready', function() {
            console.log('The widget is ready');
        });

        Bots.connect();     // Connect to server

        window[name] = Bots;
    }, 0);
}
</script>
<script src="<WebSDK URL>" onload="initSDK('<WebSDK namespace>')"></script>
```

### Keyboard Shortcuts - Hotkeys

By defining the `hotkeys` object, you can create Alt Key combination shortcuts that activate, or shift focus to, UI elements in the chat widget. Users can execute these shortcuts in place of using the mouse or touch gestures. For example, users can enter Alt + L to launch the chat widget and Alt + C to collapse it.  You assign the keyboard keys to elements using the `hotkeys` object's key-value pairs. For example:

```js
var settings = {
    // ...,
    hotkeys: {
        collapse: 'c',  // Usage: press Alt + C to collapse the chat widget when chat widget is expanded
        launch: 'l'     // Usage: press Alt + L to launch the chat widget when chat widget is collapsed
    }
};
```
When creating these key value pairs:
* You can pass only a single letter or digit for a key.
* You can use only keyboard keys a-z and 0-9.

The following table lists the keys and the corresponding elements against which you can pass the hotkey attribute. The attribute value is not case-sensitive.

| Key | Element |
|-----|---------|
| `clearHistory` | The button that clears the conversation history. |
| `close` | The button that closes the chat widget and ends conversation. |
| `collapse` | The button that collapses the expanded chat widget. |
| `input` | The text input field on the chat footer. |
| `keyboard` | The button that switches the input mode from voice to text. |
| `language` | The select menu that shows the language selection list. |
| `launch` | The chat widget launch button. |
| `mic` | The button that switches the input mode from text to voice. |
| `send` | The button that sends the input text to the skill. |
| `shareMenu` | The share menu button in the chat footer. |
| `shareMenuAudio` | The menu item in the share menu popup that selects an audio file for sharing. |
| `shareMenuFile` | The menu item in the share menu popup that selects a generic file for sharing. |
| `shareMenuLocation` | The menu item in the share menu popup that selects user location for sharing. |
| `shareMenuVisual` | The menu item in the share menu popup that selects an image or video file for sharing. |



### Customizing CSS Classes

To further customize the look of the chat widget, its CSS classes can be overridden with custom style rules. Some of the main classes are as follows:

| Class | Component |
| ------ | ------ |
| `oda-chat-wrapper` | The wrapper for entire chat widget |
| `oda-chat-button` | The chat widget launcher button |
| `oda-chat-notification-badge` | An unviewed message notification badge |
| `oda-chat-widget` | The expanded chat widget; wraps the widget header, conversation, and footer |
| `oda-chat-header` | The chat widget header |
| `oda-chat-logo` | The logo on the widget header |
| `oda-chat-title` | The title on the widget header |
| `oda-chat-connection-status` | The connection status. Each connection value has its own class as well - `oda-chat-connected`, `oda-chat-disconnected`, etc. |
| `oda-chat-connected` | Applied as a sibling to `connection-status` when the widget is connected to server |
| `oda-chat-connecting` | Applied as a sibling to `connection-status` when the widget is connecting to server |
| `oda-chat-disconnected` | Applied as a sibling to `connection-status` when the widget is disconnected from server |
| `oda-chat-closing` | Applied as a sibling to `connection-status` when the widget is disconnecting from server |
| `oda-chat-header-button` | A common class for all header buttons |
| `oda-chat-button-clear` | The clear messages button |
| `oda-chat-button-narration` | The skill audio response toggle button |
| `oda-chat-button-close` | The close widget button |
| `oda-chat-conversation` | The container for the conversation |
| `oda-chat-message` | A common wrapper class for all chat messages |
| `oda-chat-left` | The skill message wrapper |
| `oda-chat-right` | The user message wrapper |
| `oda-chat-icon-wrapper` | The skill/person icon wrapper displayed alongside message |
| `oda-chat-message-icon` | The skill/person icon image displayed alongside message |
| `oda-chat-message-bubble` | The message bubble |
| `oda-chat-message-actions` | The action buttons wrapper |
| `oda-chat-message-global-actions` | The global action buttons wrapper |
| `oda-chat-rating-star` | The rating star button in a feedback message |
| `oda-chat-rating-star-icon` | The SVG icon for the rating star button |
| `oda-chat-action-postback` | The postback action button |
| `oda-chat-action-location` | The location request action button |
| `oda-chat-card` | The card message |
| `oda-chat-footer` | The chat widget footer |
| `oda-chat-footer-button` | The common class for all footer buttons |
| `oda-chat-button-upload` | The upload file button |
| `oda-chat-button-send` | The send message button |
| `oda-chat-user-input` | the user input text area |

## Enums

The `WebSDK` object exposes various enums for the settings that support specific values. Once the library has been loaded, these enum values can be used to configure or update the SDK. The enums are:

### WebSDK.EVENT

This enum provides the event values that can be subscribed for using `Bots.on` method. The enum values are:
* `CHAT_LANG` - `'chatlanguagechange'`
* `CHAT_END` - `'chatend'`
* `CLICK_AUDIO_RESPONSE_TOGGLE` - `'click:audiotoggle'`
* `CLICK_ERASE` - `'click:erase'`
* `CLICK_VOICE_TOGGLE` - `'click:voicetoggle'`
* `DESTROY` - `'destroy'`
* `MESSAGE` - `'message'`
* `MESSAGE_RECEIVED` - `'message:received'`
* `MESSAGE_SENT` - `'message:sent'`
* `NETWORK` - `'networkstatuschange'`
* `READY` - `'ready'`
* `TYPING` - `'typing'`
* `UNREAD` - `'unreadCount'`
* `WIDGET_CLOSED` - `'widget:closed'`
* `WIDGET_OPENED` - `'widget:opened'`
* `WIDGET_SHOW` - `'widget:show'`
* `WIDGET_HIDE` - `'widget:hide'`
* `TTSStart` - `'tts:start'`
* `TTSStop` - `'tts:stop'`

The enum values can be passed to add a listener to the corresponding event. For example `Bots.on(WebSDK.EVENT.MESSAGE_SENT, function() {})` listens for sent messages. For details about each event, see [Events](#events).

### WebSDK.SPEECH_LOCALE

This enum provides the locales that are supported by the voice recognition service. The enum values are:
* `DE_DE` - `'de-de'` - German
* `EN_AU` - `'en-au'` - English (Australian)
* `EN_IN` - `'en-in'` - English (India)
* `EN_GB` - `'en-gb'` - English (UK)
* `EN_US` - `'en-us'` - English (US)
* `ES_ES` - `'es-es'` - Spanish
* `FR_FR` - `'fr-fr'` - French
* `HI_IN` - `'hi-in'` - Hindi
* `IT_IT` - `'it-it'` - Italian
* `PT_BR` - `'pt-br'` - Portuguese (Brazilian)

The enum values can be passed in the `speechLocale` setting or [setSpeechLocale(locale)](#setspeechlocalelocale) API.

> **Note**: The locales supported for voice recognition have been expanded over the versions. The following table lists locales and the first SDK version in which its support is added.

| Name | Locale | Version |
|------|--------|---------|
| English (US) | `'en-us'`  | 19.12 |
| Spanish | `'es-es' ` | 20.05 |
| French | `'fr-fr'`  | 20.05 |
| Portuguese (Brazilian) | `'pt-br'`  | 20.12 |
| German | `'de-de'`  | 21.04 |
| English (Australian) | `'en-au' ` | 21.04 |
| English (UK) | `'en-gb'`  | 21.04 |
| Italian | `'it-it'`  | 21.04 |
| English (India) |` 'en-in'`  | 21.08 |
| Hindi | `'hi-in'`  | 21.08 |

### WebSDK.THEME

This enum provides the themes that can be applied to the chat widget. The values are:
* DEFAULT - `'default'` - The default theme, provides a contrast between background layout and foreground text colors to meet [WCAG 2.1](https://www.w3.org/TR/WCAG21/) AAA requirements.
* REDWOOD_DARK - `'redwood-dark'` - Redwood dark theme, provides contrast ratio between background layout and foreground text colors to meet WCAG 2.1 AA requirements.
* CLASSIC - `'classic'` - The classic theme that was used for prior versions of the widget. Color shades have WCAG 2.1-compliant contrast as of Release 22.02.

### WebSDK.TTS

This enum provides the text-to-speech (TTS) services that are exposed . The values are:
* `platform` - The TTS service that uses platform dependent Web Speech API to synthesize text-to-speech.
* `oracle` - The default TTS service that uses OCI (Oracle Cloud Infrastructure) TTS service to generate voice for text.


The values can be passed to the `ttsService` config property during the SDK instantiation, or set dynamically by passing it to the [setTTSService(service)](#setttsserviceservice) method.

Usage:

```js
const widget = new WebSDK({
    // other config
    enableBotAudioResponse: true,
    ttsService: WebSDK.TTS.platform
});

// Set or update TTS dynamically
widget.setTTSService(WebSDK.TTS.oracle);
```

## Methods

The name that's passed in the `initSDK` parameter (WebSDK Namespace) will be used to invoke the SDK's public APIs. For example, if the name is set as `'Bots'`, the APIs can be invoked with `Bots.<API>()`.

### connect()

Connects to the current chat server.

```js
Bots.connect()
```

The API returns a `Promise` which can be used to execute code after the connection is complete or closed.

```js
Bots.connect()
    .then(
        function() {
            // Successful connection
        },
        function(error) {
            // Something went wrong during connection
        }
    )
```

### connect(config)

Connects to current chat server with passed parameters. All fields are optional, if a field is not passed and is already set from initial settings or an earlier invocation, the existing value is reused. If `userId` is not passed and is not set so far, a random userId is generated and used.

```js
Bots.connect({
    URI: '<URI>',
    channelId: '<channelId>',
    userId: '<userId>'
})
```

The API returns a `Promise` which can be used to execute code after the connection is complete or closed.

```js
Bots.connect({
    URI: '<URI>'
    channelId: '<channelId>',
    userId: '<userId>'})
    .then(
        function() {
            // Successful connection
        },
        function(error) {
            // Something went wrong during connection
        }
    )
```

The call to `connect()` API can result in a new connection or continuing existing connection depending on a few factors:
* On calling `connect()` with no parameters during no active connection, a new connection is initiated using the existing settings. For client auth enabled mode, a new token is fetched to open the connection.
* On calling `connect(param)` with parameters during no active connection, a new connection is initiated using the passed parameters. For client auth enabled mode, parameters other than `URI` are ignored, as the `channelId` and `userId` are parsed from the token.
* On calling `connect()` with no parameters during an active connection, the current connection is continued, and the returned Promise is immediately resolved.
* On calling `connect(params)` with parameters during an active connection in client auth disabled mode, if the passed parameters are the same as existing parameters, the current connection is continued.
* On calling `connect(params)` with parameters during an active connection in client auth disabled mode, if the passed parameters are different from existing parameters, the current connection is closed and a new connection is initiated with passed parameters.
* On calling `connect(params)` with parameters during an active connection in client auth enabled mode, the current connection is closed and a new connection is initiated with a new token only if a new `URI` is passed in parameters. Otherwise, the current connection is continued.


### disconnect()

Closes the currently active connection to the chat server. This includes closing the connection to the chat server, any active voice recognition, ongoing attachment uploads, and running speech synthesis.

```js
Bots.disconnect()
```

The API returns a `Promise` which is resolved when the connection is closed.

```js
Bots.disconnect()
    .then(function() {
        console.log('The connection is now closed');
    });
```

### isConnected()

Returns whether the connection to the chat server is currently active.

```js
Bots.isConnected()
```


### endChat()

Ends the current conversation session. The SDK sends an event message to the digital assistant to mark the conversation as complete. It then closes the connection, collapses the chat widget, erases the user's conversation history, and triggers the `'chatend'` event for subscribers.

```js
Bots.endChat()
```

### openChat()

Opens the chat widget popup.

```js
Bots.openChat();
```

### closeChat()

Collapses the chat widget and displays the chat icon.

```js
Bots.closeChat();
```

### isChatOpened()

Returns `true` if the widget is open. Otherwise, it returns `false`.

```js
Bots.isChatOpened();
```

### showWidget()

Displays the chat widget in its collapsed or expanded state if it is hidden from the page. The method invocation is ignored in the embedded or headless modes.

```js
Bots.showWidget();
```

### hideWidget()

Hides the chat widget in its collapsed or expanded state if it is visible on the page. The method invocation is ignored in the embedded or headless modes.

```js
Bots.hideWidget();
```

### destroy()

Destroys the SDK instance by closing any active connection, voice recognition, speech synthesis, file uploads, and by removing the widget from the UI. Once called, none of the current instance methods can be called afterward.

```js
Bots.destroy();
```

### sendAttachment(file)

Uploads file to the server. Returns a `Promise` that is resolved with the server response for successful uploads, or gets rejected with an error message for unsuccessful uploads.

```js
Bots.sendAttachment(file)
    .then(function(result) {
        console.log('File uploaded successfully.');
    })
    .catch(function(reason) {
        console.log(reason);
    });
```

### sendMessage(message, options)

Sends a message on the user’s behalf. Returns a `Promise` that is resolved with the user message on success, or gets rejected with an error message for an unsuccessful delivery or an invalid message payload. The user message is not displayed if the `Promise` is rejected.

```js
Bots.sendMessage({
    type: 'text',
    text: 'hello'
});
// OR
Bots.sendMessage('hello');
```

The messages can be sent in three formats:

* passing text string
```js
Bots.sendMessage('Show my payslip')
```

You can also pass location coordinates:

```js
Bots.sendMessage('32.323232, 143.434343')   // Latitude, longitude
```

* passing `messagePayload` of message

```js
Bots.sendMessage({
    type: 'text',
    text: 'Show menu'
})

Bots.sendMessage({
    postback: {
        variables: {},
        'system.botId': '5409672A-AB06-4109-8303-318F5EDE91AA',
        action: 'pizza',
        'system.state': 'ShowMenu'
    },
    text: 'Order Pizza',
    type: 'postback'
})
```

* passing entire message

```js
Bots.sendMessage({
    messagePayload: {
        postback: {
            variables: {},
            system.botId: '5409672A-AB06-4109-8303-318F5EDE91AA',
            action: 'pizza',
            'system.state': 'ShowMenu'
        },
        text: 'Order Pizza',
        type: 'postback'
    },
    userId: 'Guest'
})
```

To keep the message from being displayed in the widget, pass the `hidden` boolean flag in the options object.

```js
Bots.sendMessage('What is the menu today?', { hidden: true });
```

The above call will send the message to the server without displaying it in the widget.

### sendUserTypingStatus(status, userText)

Sends the user's typing status to the agent. The status can be either `RESPONDING` or `LISTENING`, where `RESPONDING` represents the user typing activity. Use this API to send the user typing status when running in headless mode.

```js
Bots.sendUserTypingStatus('RESPONDING', 'Hello!'); // Send typing status for the user with the user text `Hello!`

Bots.sendUserTypingStatus('LISTENING'); // Send listening status for the user
```

### updateUser(userDetails)

Updates the user information.

```js
Bots.updateUser({
    messagePayload: {
        text: 'give me a pizza',
        type: 'text'
    },
    profile: {
        firstName: 'Jane',
        lastName: 'Smith',
        email: 'updated@email.com',
        properties: {
            justGotUpdated: true
        }
    }
});
```

> **Note**: You can also use the `initUserProfile` property to set profile values. If you use the `initUserHiddenMessage` property, and the response from the server is expected to have user profile values, then you must use the `initUserProfile` property instead of setting the values in `updateUser()`. For later updates to the user profile, use `updateUser()`.

### setUserAvatar(userAvatar)

Sets the user avatar. The value passed must be the URL of the image source, or the source string of the SVG image that should be displayed alongside the user messages.

```js
Bots.setUserAvatar('../assets/images/avatar-user.jpg');
```

### setAgentDetails(agentDetails)

Sets the current agent details that should be displayed for agent messages. If there is an agent handover, the latest agent details will replace the details set by this API. All fields are optional, so if a field is not passed and is already set from the initial settings or an earlier invocation, the existing value is reused. The value passed for `avatarImage` must be the URL of the image source, or the source string of the SVG image that should be displayed alongside the agent messages. The values passed for `nameTextColor`, `avatarTextColor`, and `avatarBackgroundColor` must be in standard [color](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value) format.

```js
Bots.setAgentDetails({
    name: 'Ana Lee',
    avatarImage: '../assets/images/avatar-agent.jpg',
    nameTextColor: 'rgba(22, 21, 19, 0.65)',
    avatarTextColor: 'green',
    avatarBackgroundColor: '#A890B6'
});
```

> **Note**: This API does not change the previous agent details. These passed values will have the lifetime of the current agent session only.

### getAgentDetails()

Returns the current agent details.

```js
Bots.getAgentDetails();
```

### getSuggestions(query)

If the autocomplete feature is enabled (`enableAutocomplete: true`), this API returns a `Promise` that resolves to the suggestions for the given query string. If it takes too long (~10s) to fetch the suggestion, the `Promise` is rejected.

```js
Bots.getSuggestions('pizza')
    .then(function(suggestions) {
        var suggestionString = suggestions.toString();
        console.log('The suggestions are: ', suggestionString);
    })
    .catch(function(reason) {
        console.log('Suggestion request failed', reason);
    });
```

The API expects a single query string parameter and returns a `Promise`. On a successful request for suggestions, the `Promise` is resolved to a string array. On failure, the `Promise` is rejected with an error message.

If the API is called when the feature is disabled, it returns a rejected Promise.

### startVoiceRecording(onSpeechRecognition, onSpeechNetworkChange, options)

Starts the voice recording if the speech recognition feature is enabled. The API returns a `Promise` that is resolved when the speech service starts recording. In case of an error, the `Promise` is rejected with an Error object.
The API expects two callbacks to be passed as its parameters:
`onSpeechRecognition` function is called on the speech server response. The JSON response is passed as a parameter.
`onSpeechNetworkChange` function is called on a change in the speech connection. A single parameter, the WebSocket status, is passed.

```js
Bots.startVoiceRecording(function(data) {
    var recognizedText = '';
    if (data && (data.event === 'finalResult' || data.event === 'partialResult')) {
        if (data.nbest && data.nbest.length > 0) {
            recognizedText = data.nbest[0].utterance;
        }
    }
}, function(status) {
    if (status === WebSocket.OPEN) {
        // Connection established
    } else if (status === WebSocket.CLOSED) {
        // Connection closed
    }
})
```

The function also accepts an optional `options` object that can have fields for two callback functions for the analyser - `onAnalyserReady`, and `onAnalyserFrequencies`. Either one, or both, fields can be passed.
These callbacks can be used to get regular frequency values for visualization.

`onAnalyserReady` is a one-time callback that is called when the analyser node is initialized. The callback method is passed as a single argument, an [`AnalyserNode`](https://developer.mozilla.org/en-US/docs/Web/API/AnalyserNode/), which is configured with a `fftSize` of 256, and connected to the voice input source.

`onAnalyserFrequencies` is a callback method that is called every time a new set of voice input frequencies are provided by the analyser node. The callback method is passed a single argument, an `Uint8Array` of size 128, depicting the frequency data composed of integers on a scale from 0 to 255. Each item in the array represents the decibel value for a specific frequency. The frequencies are spread linearly from 0 to 1/2 of the sample rate. For example, for the 48000 sample rate, the last item of the array will represent the decibel value for 24000 Hz.

```js
Bots.startVoiceRecording(function(data) {
    var recognizedText = '';
    if (data && (data.event === 'finalResult' || data.event === 'partialResult')) {
        if (data.nbest && data.nbest.length > 0) {
            recognizedText = data.nbest[0].utterance;
        }
    }
}, function(status) {
    if (status === WebSocket.OPEN) {
        // Connection established
    } else if (status === WebSocket.CLOSED) {
        // Connection closed
    }
}, {
    onAnalyserReady: function(analyserNode) { console.log('The analyser node is', analyserNode); },
    onAnalyserFrequencies: function(frequencies) { console.log('New input frequencies are', frequencies); }
})
```

### stopVoiceRecording()

Stops any running voice recording. Throws an error if speech recognition is not enabled.

```js
Bots.stopVoiceRecording()
```

### setSpeechLocale(locale)

Sets the locale used for speech connection. The user is expected to speak with the same locale that is set here to the SDK. The list of currently supported locales is available at [WebSDK.SPEECH_LOCALE](#websdkspeech_locale). If an unsupported locale is passed, the API returns `false` while maintaining the passed locale. In such a case, any voice recognition attempt is failed.
The function returns a boolean indicating whether the passed locale is supported or not.

```js
Bots.setSpeechLocale('fr-fr');
```

> **Note**: When both voice recognition and audio response are enabled but the audio response locale is not set, then the locale for the audio response voice gets set to the same locale as the voice recognition locale.

Example:
```js
var Bots = new WebSDK({
    // ...,
    enableSpeech: true,
    enableBotAudioResponse: true
});

// ...

Bots.setSpeechLocale('es-es');

```

In the above example, the locale for audio response voice is set to `'es-es'` automatically.

### setPrimaryChatLanguage(languageTag)

Updates the language selected for the conversation between the user and the skill in the selection dropdown. This function can only be called when the multi-lingual chat feature is configured.

```js
Bots.setPrimaryChatLanguage('fr')
```

If the passed language tag does not match any of the passed supported languages, `Detect Language` is set and skill determines which language is being used for conversation.

### setSkillVoices(voices)

**Deprecated** - This method has been deprecated in favor of [setTTSVoice(voices)](#setttsvoicevoices), and will be removed in upcoming releases.

Dynamically updates the synthesis voice used to narrate skill messages. The function can accept a single `skillVoice` object or an array of `skillVoice` objects. The function returns a `Promise` which resolves to the skill voice that is applied to the synthesis service. It can be one of the passed voices or a fallback when none of the passed voices are available on the device. The `Promise` is rejected if the skill audio response feature is not enabled.


```js
Bots.setSkillVoices({ lang: 'fr-fr' });

Bots.setSkillVoices({ lang: 'fr-fr', name: 'Thomas' })

Bots.setSkillVoices([{
    lang: 'es-mx',
    name: 'Juan'
}, {
    lang: 'es-es',
    name: 'Monica'
}, {
    lang: 'es-ar',
    name: 'Diego'
}, {
    lang: 'es-es'
}])
```

### setTTSService(service)

Injects a TTS service that is used by the SDK for the utterance of incoming skill messages. The passed service object needs to implement the [SpeechSynthesisService](#speech-synthesis-service-interface) interface to have the functions that the SDK requires to utilize it. If an invalid or empty service object is passed, the synthesis service is disabled. See [Speech Synthesis Service Injection](#speech-synthesis-service-injection) for more details.

```js
var myOwnTTSService = {
    /**
     * Adds a phrase to the utterance queue to be spoken
     *
     * @param {string} phrase
     */
    speak: function(phrase) {},

    /**
     * Cancels any ongoing speech synthesis utterance
     */
    cancel: function() {},

    /**
     * Returns a Promise that resolves into a list of SpeechSynthesisServiceVoice objects representing
     * the available voices
     *
     * @return {*}  {Promise<SpeechSynthesisServiceVoice[]>}
     */
    getVoices: function() {},

    /**
     * Sets the voice to be used for speaking the utterances. It accepts an array of candidate voices
     * sorted in their preference order, and sets one of them according to its matching criteria.
     * It returns a Promise that gets resolved when the voice is set.
     *
     * @param {SpeechSynthesisServiceVoice[]} voice
     * @return {*}  {Promise<void>}
     */
    setVoice: function(voices) {},

    /**
     * Returns the voice that is currently used for speaking utterances
     *
     * @return {*}  {SpeechSynthesisServiceVoice}
     */
    getVoice: function() {}
};

Bots.setTTSService(myOwnTTSService);
```

You can also pass the `WebSDK.TTS` values to the `setTTSService` method to set them as the TTS service used by the SDK.

```js
Bots.setTTSService(WebSDK.TTS.oracle);      // Sets the OCI TTS service
Bots.setTTSService(WebSDK.TTS.platform);    // Sets the platform based TTS service
```

### getTTSVoices()

Returns a `Promise` that resolves into a list of [SpeechSynthesisServiceVoice](#speech-synthesis-service-interface) objects representing the available voices for speech synthesis. When using SDK's native speech synthesis service, this list is populated with the voices provided by the platform/OS. When using a third-party synthesis service, the list is populated by the voices that are provided by that service.

```js
Bots.getTTSVoices()
    .then(function(voices) {
        console.log(voices);
    });

/**
 * [
 * {
 *      default: false,
 *      lang: "en-US",
 *      localService: true,
 *      name: "Alex",
 *      voiceURI: "urn:moz-tts:osx:com.apple.speech.synthesis.voice.Alex"
 * },
 * {
 *      default: false,
 *      lang: "it-IT",
 *      localService: true,
 *      name: "Alice",
 *      voiceURI: "urn:moz-tts:osx:com.apple.speech.synthesis.voice.alice"
 * },
 * {
 *      default: false,
 *      lang: "sv-SE",
 *      localService: true,
 *      name: "Alva",
 *      voiceURI: "urn:moz-tts:osx:com.apple.speech.synthesis.voice.alva"
 * }...
 * ]
 * /
```

### setTTSVoice(voices)

Sets the voice that's used for speaking the skill's utterances. It accepts an array of candidate voices that's sorted by preference. From this array, it either sets the first voice that's provided by the synthesis service as the skill's voice, or it sets a voice that closely matches one of the voices available in the synthesis service. It returns a `Promise` that gets resolved when the voice is set.

This function is similar to [setSkillVoices(voices)](#setskillvoicesvoices) and will be the preferred method in coming releases.

```js
Bots.setTTSVoice([{
    lang: 'es-mx',
    name: 'Juan'
}, {
    lang: 'es-es',
    name: 'Monica'
}, {
    lang: 'es-ar',
    name: 'Diego'
}, {
    lang: 'es-es'
}]).then(function() {
    Bots.speak('Hello');
});
```

### getTTSVoice()

Returns the voice that is currently used by the synthesis service for speaking utterances. It returns a [SpeechSynthesisServiceVoice](#speech-synthesis-service-interface) object representing the selected voice.

```js
var currentVoice = Bots.getTTSVoice();
console.log(currentVoice);
/**
 * {
 *      default: false,
 *      lang: "en-US",
 *      localService: true,
 *      name: "Alex",
 *      voiceURI: "urn:moz-tts:osx:com.apple.speech.synthesis.voice.Alex"
 * }
 * /
```

### speakTTS(phrase)

Calls the speech synthesis service to speak the passed phrase. The passed phrase can either be a plain string, or a skill message object received from the server.

```js
Bots.speakTTS('Hello World');

var skillMessage = {
    messagePayload: {
        type: 'text',
        text: 'What is your order number?'
    }
};

Bots.speakTTS(skillMessage);    // Will utter 'What is your order number?'
```

### cancelTTS()

Cancels any ongoing utterance from the speech synthesis service.

```js
Bots.cancelTTS();
```

### setDelegate(delegate)

The `setDelegate` method can be used to change or remove delegate callbacks after a conversation has been initialized. If no value is passed, the existing delegates are removed.

```js
Bots.connect().then(function() {
    Bots.setDelegate({
        beforeDisplay(message) {
            return message;
        },
        beforeSend(message) {
            return message;
        },
        beforePostbackSend(postback) {
            return postback;
        },
        beforeEndConversation(message) {
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve(message);
                }, 2000);
            });
        },
        render(message) {
            if (message.messagePayload.type === 'card') {
                // Perform custom rendering for card using msgId
                return true;
            }
            return false;
        }
    })
});
```

### getConversationHistory()

Returns information about the current conversation for the user. The response is an object containing user ID, messages, and unread message count.

```js
Bots.getConversationHistory()

{
    messages: [
        {
            date: '2020-01-22T17:06:24.085Z',
            isRead: true,
            messagePayload: {
                text: 'show menu',
                type: 'text'
            },
            userId: 'user74882436'
        }
    ],
    messageCount: 1,
    unread: 0,
    userId: 'user74882436'
}
```

### clearConversationHistory(userId, shouldClearWidget)

This API clears the conversation history for a known user from the browser's localStorage. The `userId` must be a string. On passing an empty or no userId, the current user's history is removed.

If the passed `userId` is the same as the current user's `userId`, then you can also pass an optional boolean argument, `shouldClearWidget`, to configure whether the current chat widget UI should also be cleared on calling this API. By default, the value is `true`.

> **Note**: This API does not interact with `sessionStorage` for users other than the current user. The `sessionStorage` is automatically cleared on closing the tab.

```js
Bots.clearConversationHistory('Jonathan');      // Removes conversation history of Jonathan

Bots.clearConversationHistory('Adriana');       // Removes conversation history of Adriana and clears the widget UI if Adriana is current user

Bots.clearConversationHistory('', false);       // Removes conversation history of current user without clearing the widget UI
```

### clearAllConversationsHistory(shouldClearWidget)

This API clears the conversation history for all users from the browser's localStorage. Like `clearConversationHistory`, this method can also help in recovering significant portions of localStorage from the user's browser.

You can also pass an optional boolean argument, `shouldClearWidget`, to configure whether the current chat widget UI should also be cleared on calling this API. By default, the value is `true`.

> **Warning** - The actions taken by calling this API cannot be undone. Once the messages are deleted, they cannot be recovered. Call this method sparingly and only when absolutely needed.

> **Note**: This API does not interact with `sessionStorage` for users other than the current user. The `sessionStorage` is automatically cleared on closing the tab.

```js
Bots.clearAllConversationsHistory()
```

### getUnreadMessagesCount()

Returns the count of the unread messages.

```js
Bots.getUnreadMessagesCount();
```

### setAllMessagesAsRead()

Marks all messages as have been read/seen by the user.

```js
Bots.getUnreadMessagesCount(); // 2
Bots.setAllMessagesAsRead();
Bots.getUnreadMessagesCount(); // 0
```

### setUserInputMessage(text)

Populates the user input field with the passed message.

```js
Bots.setUserInputMessage('Show my agenda for today please.');
```

### setUserInputPlaceholder(text)

Updates user input's placeholder text. It can be used to change the placeholder text according to the input expected from the user.

```js
Bots.setUserInputPlaceholder('Add your pizza topping');
```

### showTypingIndicator()

Displays the typing indicator in the conversation. If the typing indicator is already visible, then the timer to hide it gets reset. The typing indicator is automatically removed if the server sends a response, or the timer period set by `typingIndicatorTimeout` (in seconds) has expired.

The method only works if the `showTypingIndicator` setting is set to `true`, the SDK is *not* in headless mode, and the widget is connected to the server.

```js
Bots.showTypingIndicator();
```


### setWebViewConfig(webViewConfig)

Sets and updates the Webview configuration, customizing the Webview component. Check out the [In-Widget Webview](#in-widget-webview) section under customization for more details.

```js
Bots.setWebViewConfig({
    accessibilityTitle: 'Webview container for Wikipedia',
    sandbox: ['allow-scripts', 'allow-downloads'],
    size: 'tall',
    title: 'Wikipedia'
});
```

### setChatBubbleIconHeight(height)

Sets the height of the loading chat bubble icon. The height must be provided as a string value in one of the standard [length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) units.

```js
Bots.setChatBubbleIconHeight('18px');
```

### setChatBubbleIconWidth(width)

Sets the width of the loading chat bubble icon. The width must be provided as a string value in one of the standard [length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) units.

```js
Bots.setChatBubbleIconWidth('24px');
```

### setChatBubbleIconSize(width, height)

Sets the size of the loading chat bubble icon. The width and height must be provided as string values in one of the standard [length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) units.

```js
Bots.setChatBubbleIconSize('24px', '18px');
```

### setFont(font)

Sets the font for the chat widget. The syntax of the `font` must follow the [standard pattern](https://developer.mozilla.org/en-US/docs/Web/CSS/font).

```js
Bots.setFont('14px italic large sans-serif');
```

### setFontFamily(fontFamily)

Set font family used for all text content in the chat widget. The `fontFamily` argument must be a string and follow the [standard pattern](https://developer.mozilla.org/en-US/docs/Web/CSS/font-family).

```js
Bots.setFontFamily('"Gill Sans", sans-serif');
```

### setFontSize(fontSize)

Sets the font size for the text in the chat widget. The syntax of `fontSize` must follow the standard [permissible values](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size).

```js
Bots.setFontSize('16px');
```

### setHeight(height)

Sets the height of the chat widget. The value passed must be in one of the [length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) units.

```js
Bots.setHeight('786px')
```

### setWidth(width)

Sets the width of the chat widget. The value passed must be in one of the [length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) units.

```js
Bots.setWidth('320px')
```

### setSize(width, height)

Sets the size of the chat widget. The values passed must be in one of the [length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) units.

```js
Bots.setSize('320px' ,'786px',)
```

### setMessagePadding(padding)

Sets the padding around the message in the chat widget. The syntax of `padding` must follow standard [permissible values](https://developer.mozilla.org/en-US/docs/Web/CSS/padding).

```js
// Apply padding to all four sides
Bots.setMessagePadding('15px');
// vertical | horizontal
Bots.setMessagePadding('5% 10%');
// top | horizontal | bottom
Bots.setMessagePadding('15em 20em 20em');
// top | right | bottom | left
Bots.setMessagePadding('15px 20px 20px 15px');
```

### setTextColor(color)

Sets the primary text color of messages in the chat widget. It does not modify the colors in actions. The value passed must be in standard [color](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value) format.

```js
Bots.setTextColor('#33ee00')
```

### setTextColorLight(color)

Sets the color of the secondary messages in the chat widget, like descriptions. The value passed must be in standard [color](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value) format.

```js
Bots.setTextColorLight('rgb(13, 155, 200)')
```


## Events

To bind an event, use `Bots.on(<event name>, <handler>)`. To unbind events, you can either:
* Call `Bots.off(<event name>, handler)` to remove one specific handler.
* Call `Bots.off(<event name>)` to remove all handlers for an event.
* Call `Bots.off()` to unbind all handlers.

We recommend adding event handlers before calling the `connect()` method so that they can be registered and triggered appropriately.

### ready

This event is triggered when connect completes successfully. Be sure to bind before calling connect.

```js
Bots.on('ready', function(){
    console.log('the init has completed!');
});
```

Listeners to the `ready` event must be added before calling the `connect()` method. Otherwise, the listeners will not be registered in time to be triggered.

### destroy

This event is triggered when the widget is destroyed.
```js
Bots.on('destroy', function(){
    console.log('the widget is destroyed!');
});
Bots.destroy();
```

### message:received

This event is triggered when the user receives a message. If [beforeDisplay](#beforedisplay) delegate is set, the callback would receive the message to be displayed after executing the delegate.
```js
Bots.on('message:received', function(message) {
    console.log('the user received a message', message);
});
```

### message:sent

This event is triggered when the user sends a message. If [beforeSend](#beforesend) delegate is set, the callback would receive the message sent to the server after executing the delegate.
```js
Bots.on('message:sent', function(message) {
    console.log('the user sent a message', message);
});
```

### message

This event is triggered when a message is added to the conversation.
```js
Bots.on('message', function(message) {
    console.log('a message was added to the conversation', message);
});
```

### networkstatuschange

This event is triggered whenever the network status of the connection to the server changes. The callback receives a status number parameter, which corresponds to [WebSocket network status constants](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket#Constants).
```js
Bots.on('networkstatuschange', function(status) {
    switch (status) {
        case 0:
            status = 'Connecting';
            break;
        case 1:
            status = 'Open';
            break;
        case 2:
            status = 'Closing';
            break;
        case 3:
            status = 'Closed';
            break;
    }
    console.log(status);
});
```

### typing

This event is triggered whenever the user starts or stops typing in the user input field. The listener receives a boolean parameter, which is set `true` when the user starts typing and set `false` when `typingStatusInterval` has elapsed after the user stops typing.
```js
Bots.on('typing', function(isTyping) {
    console.log('User currently typing: ', isTyping);
});
```

### unreadCount

This event is triggered when the number of unread messages changes.
```js
Bots.on('unreadCount', function(unreadCount) {
    console.log('the number of unread messages was updated', unreadCount);
});
```

### widget:opened

This event is triggered when the widget is opened.
```js
Bots.on('widget:opened', function() {
    console.log('Widget is opened!');
});
```

### widget:closed

This event is triggered when the widget is closed.
```js
Bots.on('widget:closed', function() {
    console.log('Widget is closed!');
});
```

### widget:show

This event is triggered when the widget is toggled to be shown with `showWidget()` method.
```js
Bots.on(WebSDK.EVENT.WIDGET_SHOW , function() {
    console.log('Widget is visible.');
});
```

### widget:hide

This event is triggered when the widget is toggled to be hidden with `hideWidget()` method.
```js
Bots.on(WebSDK.EVENT.WIDGET_HIDE, function() {
    console.log('Widget is hidden.');
});
```

### click:audiotoggle

This event is triggered when the audio utterance of response is toggled. The subscribers receive the boolean status - `true` if the audio response is turned on, `false` if it is turned off.
```js
Bots.on('click:audiotoggle', function(status) {
    if (status === true) {
        console.log('Audio response is turned on.');
    } else {
        console.log('Audio response is turned off.');
    }
})
```

### click:erase

This event is triggered when the erase conversation history button is clicked. No parameters are passed to the subscribers.
```js
Bots.on('click:erase', function() {
    console.log('Conversation history is erased.');
})
```

### click:voicetoggle

This event is triggered when the voice activation button is toggled. The subscribers receive the boolean status - `true` if the voice is activated, `false` if it is deactivated.
```js
Bots.on('click:voicetoggle', function(status) {
    if (status === true) {
        console.log('Voice recording is started.');
    } else {
        console.log('Voice recording is stopped.');
    }
})
```

### chatlanguagechange

This event is triggered when the chat language in language selection dropdown is selected or changed. This dropdown is exposed on enabling the [Multi-Lingual Chat](#multi-lingual-chat) feature. Its subscribers receive the selected language's language tag. If auto-detect is selected, `null` is passed as the argument.


```js
Bots.on('chatlanguagechange', function(language) {
    console.log('The selected chat language is', language);
});
```

### chatend

This event is triggered when the conversation is ended.

```js
Bots.on('chatend', function() {
    console.log('The conversation is ended.');
});
```

### TTSStart

This event is triggered when the TTS is started.

```js
Bots.on(WebSDK.EVENT.TTSStart, function() {
    console.log('The TTS is started.');
});
```

### TTSStop

This event is triggered when the TTS is stopped or ended.

```js
Bots.on(WebSDK.EVENT.TTSStop, function() {
    console.log('The TTS is ended.');
});
```

## Features

### Autocomplete

Feature Flag: `enableAutocomplete: true` (default: `false`)

Enable client side caching: `enableAutocompleteClientCache`

Autocomplete provides suggestions to end users to better form the utterance and select the specific entity value. To enable autocomplete, you must add autocomplete suggestions to the skill's intents. Then, whenever the user types a character in the input field, the intents' autocomplete suggestions display in a popup to suggest the best format, helping to minimize user errors. An intent's autocomplete suggestions should not be a full word dictionary. Their purpose is to minimize the scope and allow better guidance to the end user.

The feature can also be used in headless mode using `getSuggestions()` API. The API details are described in the Method section above.

> **Note**: This feature is only available over WebSocket.

### Auto-Submit

* This feature is used in Edit-Form messages. When an editable field has the `autoSubmit` property set to `true`, the client sends a [FormSubmissionMessagePayload](#user-form-submission-message) with the `submittedField` map containing the valid field values that have been entered so far.
* Any fields that have not yet been set -- regardless of whether they are required --  or fields that violate a client-side validation, are not included in the `submittedField` map.
* If the auto-submitted field itself contains an invalid value, then the form submission message is not sent, and the client error message displays for that particular field.
* In case of a successful auto-submit, the `partialSubmitField` in the form submission message will be set to the `id` of the autoSubmit field.

### Replacing Previous Edit-Form

* This feature is used in Edit-Form messages. When the end user submits the editable form, either because a field has [autoSubmit](#auto-submit) set to `true`, or the user has used the `SubmitForm` action button, there might be situations in which the user did not provide all the required information, and/or some field values contain an invalid value.
* In such a case, the skill can send a new `EditFormMessagePayload`, but that message should replace the previous Edit-Form message.
* When the skill configures the `replaceMessage` channel extension property to `true`, SDK replaces the previous Edit-Form message with the current Edit-Form message.

### Delegation

Feature configuration: `delegate`

The delegation feature enables you set a delegate to receive callbacks before certain events in the conversation. To set a delegate, pass it in the `delegate` property or use the `setDelegate` method. The delegate object may optionally contain `beforeDisplay`, `beforeSend`, `beforePostbackSend`, `beforeEndConversation` and `render` delegate functions.

```js
var delegate = {
    beforeDisplay: function(message) {
        return message;
    },
    beforeSend: function(message) {
        return message;
    },
    beforePostbackSend: function(postback) {
        return postback;
    },
    beforeEndConversation: function(message) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(message);
            }, 2000);
        });
    },
    render: function(message) {
        if (message.messagePayload.type === 'card') {
            // Perform custom rendering for card using msgId
            return true;
        }
        return false;
    }
}

Bots.setDelegate(delegate);
```

#### beforeDisplay

The `beforeDisplay` delegate allows a skill message to be modified before it is displayed in the conversation. The message returned by the delegate displays instead of the original message. The returned message is not displayed if the delegate returns a falsy value like `null`, `undefined`, or `false`. If the delegate errors out, then the original message will be displayed instead.

#### beforeSend

The `beforeSend` delegate allows a user message to be modified before it is sent. The message returned by the delegate is sent to the skill instead of the original message. The message returned by the delegate is not sent if the delegate returns a falsy value like `null`, `undefined`, or `false`. If the delegate errors out, the original message will be sent instead.

#### beforePostbackSend

The `beforePostbackSend` delegate is similar to `beforeSend` but is instead applied to postback messages from the user. The postback returned by the delegate is sent to the skill. The postback returned by the delegate is not sent if the delegate returns a falsy value like `null`, `undefined`, or `false`. If the delegate errors out, the original postback will be sent instead.

#### beforeEndConversation

The `beforeEndConversation` delegate allows an interception the end conversation flow if some pre-exit activity must be performed. The function receives the exit message as its input parameter. It must return a `Promise`. If this `Promise` resolves with the exit message, then the `CloseSession` exit message is sent to the chat server. Otherwise, the exit message is prevented from being sent.

#### render

The `render` delegate allows to override the default message rendering. If the `render` delegate function returns `true` for a particular message type, then the WebSDK creates a placeholder slot instead of default message rendering. To identify the placeholder, the WebSDK adds the `msgId` of the message as the `id` of the element. In the `render` delagate function, you can use this identifier to get the reference for the placeholder and render your custom message template. See [Custom Message Rendering](#custom-message-rendering) for more details.


### Embedded Mode

Feature flag: `embedded: true` (default: `false`)

Pass ID of target container element: `targetElement`

The chat widget appears as a fixed position element on the bottom right of the page, which does not respond to gestures on the page. But it can also be embedded into the host and become part of the page. To activate the embedded mode, you need to pass `embedded: true`, and provide a target container with `targetElement: <targetDivId>`. This accepts a DOM element that will be used as the container where the widget will be rendered.

The embedded widget occupies the full width and height of the container. A height and width must be specified for the target element. Otherwise, the widget will collapse.


### Headless SDK

Feature flag: `enableHeadless: true` (default: `false`)

Similar to headless browsers, the SDK can also be used without a UI. The SDK maintains the connection to the server, and provides APIs to send messages, receive messages, and get updates of the network status. Developers can use the APIs to interact with the SDK, and update UI appropriately.

The communication can be implemented as follows:
* Sending messages - Call `Bots.sendMessage(message)` to pass any payload to server.
* Receiving messages - Response can be listened for using `Bots.on('message:received', <messageReceivedCallbackFunction>)`.
* Get connection status update - Updates to status of the connection to server can be listened for using `Bots.on('networkstatuschange', <networkStatusCallbackFunction>)`. The callback has a parameter `status`, which is updated with values from 0 to 3. These values map to [WebSocket states](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket#Constants):
  * 0 - `WebSocket.CONNECTING` - Connecting
  * 1 - `WebSocket.OPEN` - Open
  * 2 - `WebSocket.CLOSING` - Closing
  * 3 - `WebSocket.CLOSED` - Closed
* Check if connection is open - Call `Bots.isConnected()` to check if the connection is open or not.
* Get suggestions list - If autocomplete is enabled, call `Bots.getSuggestions(query)` where query is the string to get the suggestions list.


### In-Widget Webview

Feature flag: `linkHandler: { target: 'oda-chat-webview' }`

Feature configuration: `webViewConfig`

Public method: `setWebViewConfig(webViewConfig)`

The Web SDK contains an in-widget Webview component that can be used to view the message links within the chat widget. This feature allows users to interact with links in the conversation without taking them away from the widget to a new tab or window. The in-widget Webview can be applied globally to open all links in the messages inside it, or can be selectively configured for specific links.

To open all links in the conversation in the Webview, you just need to pass `linkHandler: { target: 'oda-chat-webview' }` in the settings. This sets the target of all links to `oda-chat-webview`, which is the name of the Webview iframe.

In more general scenarios, you'll probably need to open only certain links in the Webview, while ensuring other links open normally in other tabs/windows. The `beforeDisplay` delegate can be used to make that work. To open a specific message URL action in the Webview, replace `action.type` field's value from `url` to `webview`. Once the action type is changed to `webview` in `beforeDisplay`, clicking that action button will open the link in the Webview.
Opening specific links embedded in the text in Webview is a bit more challenging. The embedded link needs to be converted into an anchor element (\<a href="https://www.oracle.com"\>), and the `target="oda-chat-webview"` attribute should be added in that anchor element.

The `webViewConfig` setting allows customizing the Webview component. It accepts an object that can have the following optional fields:
```js
{
    accessibilityTitle: string,                             // Name of Webview frame element for Web Accessibility
    closeButtonIcon: string,                                // Image URL/SVG string that is used to display the close button icon
    closeButtonLabel: string,                               // Text label/tooltip title for the close button
    closeButtonType: 'icon' | 'label' | 'iconWithLabel',    // Sets how the close button is displayed in the Webview
    errorInfoBar: boolean,                                  // Sets to display or hide fallback view with original URL
    errorInfoDismissLabel: string,                          // Label for error-view bar dismiss button
    errorInfoText: string,                                  // Informational text displayed in an error-view bar inside Webview as a fallback for the user in case the URL fails to load in the Webview
    referrerPolicy: ReferrerPolicy                          // Indicates which referrer to send when fetching the frame's resource
    sandbox: string[],                                      // Array of extra restrictions to the content in the Webview frame
    size: 'tall' | 'full',                                  // Height of the Webview compared to chat widget. When set 'tall', it is set as 80%, 100% for 'full'.
    title: string                                           // Webview title shown on the header of the Webview container
}
```

The `referrerPolicy` policy value passed should be a [valid directive](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy#Directives). The default policy applied is `'no-referrer-when-downgrade'`.

The `sandbox` field accepts an array of valid restriction strings that allows for the exclusion of certain actions inside the frame. The restrictions that can be passed to the field can be found under the sandbox attribute manual at [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe).

The configuration can also be updated dynamically by passing a `webViewConfig` object in the method `setWebViewConfig()`. Every property in the object is optional.

The Webview optionally presents a fallback view that contains the original URL link as a fallback in case the page fails to load inside the Webview. Clicking the link in this view opens the page in a new tab. The informational text can be customized with the `webViewErrorInfoText` `i18n` translation string and must contain a placeholder text for the link label. For example:
```js
settings = {
    URI: 'instance',
    //...,
    i18n: {
        en: {
            webViewErrorInfoText: 'This link can\'t be opened here. You can open it in a new page by clicking {0}here{/0}.'
        }
    }
}
```
This error view can be disabled by passing `errorInfoBar: false` in the `webViewConfig` setting.

**Limitations**
1. Pages that provide response header `X-frame-options: deny` or `X-frame-options: sameorigin` may not open in the Webview due to server-side restrictions preventing the page to be opened inside iframes. The Webview presents a dismissible popup with a link back to the user in the Webview. Users can open it in a new window or tab by clicking it.
2. Due to the above restrictions, authorization pages like IDCS, Google Login, FB Login, etc. can not be opened inside the WebViews, as authorization pages always return `X-frame-options: deny` to prevent [clickjacking](https://tools.ietf.org/html/draft-ietf-oauth-v2-23#section-10.13).
3. Only links inside the conversation messages can be opened inside the Webview. Any external links must not be targeted to be opened in the Webview, clicking on such links won't open the Webview correctly.


### Long Polling

Feature flag: `enableLongPolling: true` (default: `false`)

The SDK uses WebSockets to connect to the server and converse with skills. If for some reason the WebSocket is disabled over the network, traditional HTTP calls can be used to chat with the skill. This feature is known as long polling, as the SDK has to continuously call or poll the server to fetch the latest messages from the skill.

Long polling provides fallback support for conversations on browsers that don't have WebSockets enabled or blocked.


### Multi-Lingual Chat

The Web SDK's native language support enables the chat widget to detect a user's language or allow users to select the converation language.

#### Enable the Language Menu

You can enable a menu that allows users to select a preferred language from a dropdown menu by defining the `multiLangChat` property with an object containing the `supportedLangs` array, which is comprised of language tags (`lang`) and optional display labels (`label`) to override the default translation strings. Outside of this array, you can optionally set the default language with the primary key (`primary: 'en'` in the following snippet). If the primary key matches one of the supported languages, then that language is selected. When no match can be found, **Detect Language** is activated.

```js
multiLangChat: {
    supportedLangs: [{
        lang: 'en'
    }, {
        lang: 'es',
        label: 'Español'
    }, {
        lang: 'fr',
        label: 'Français'
    }, {
        lang: 'hi',
        label: 'हिंदी'
    }],
    primary: 'en'
}
```
The chat widget displays the passed-in supported languages in a dropdown menu that's located in the header. In addition to the available languages, the menu also includes a **Detect Language** option. When a user selects a language from this menu, the current conversation is reset, and a new conversation is started with the selected language. The language selected by the user persists across sessions in the same browser, so the user's previous language is automatically selected when the user revisits the skill through the page containing the chat widget.

You can add an event listener for the `chatlanguagechange` event, which is triggered when a chat language has been selected from the dropdown menu or has been changed.

```js
Bots.on('chatlanguagechange', function(language) { console.log('The selected chat language is', language); });
```
#### Disable Language Menu

Starting with Version 21.12, you can also configure and update the chat language without also having to configure the language selection dropdown menu by passing `multiLangChat.primary` in the initial configuration without also passing a `multiLangChat.supportedLangs` array. The value passed in the primary variable is set as the chat language for the conversation.

#### Language Detection

In addition to the passed in languages, the chat widget displays a **Detect Language** option in the dropdown. Selecting this option tells the skill to automatically detect the conversation language from the user's message and, when possible, to respond in the same language.

If you omit the primary key or if the primary key is invalid, the widget automatically detects the language in the user profile and activates the **Detect Language** option in the menu.
You can dynamically update the selected language by calling the `setPrimaryChatLanguage(lang)` API. If the passed `lang` matches one of the supported languages, then that language is selected. When no match can be found, **Detect Language** is activated. You can also activate the **Detected Language** option by calling `setPrimaryChatLanguage('und')` API, where `'und'` indicates undetermined or by passing either `multiLangChat: {primary: null}` or `multiLangChat: {primary: 'und'}`.
You can update the chat language dynamically using the `setPrimaryChatLanguage(lang)` API even when the dropdown menu has not configured. For example:

```js
Bots.setPrimaryChatLanguage('fr')
```

You can dynamically update the language irrespective of whether the chat language is initially configured or not.

Response narration and voice recognition, when configured, are available when users select a supported language. They are not available when the **Detect Language** option is set. Selecting a language that is not supported by voice recognition disables the recognition functionality until a supported language has been selected.

#### Multi-Lingual Chat Quick Reference

| To do this... | ...Do this |
| ------ | ------ |
| Display the language selection dropdown to end users.| Pass `multiLangChat.supportedLangs`.|
| Set the chat language without displaying the select language selection dropdown menu to end users.| Pass `multiLangChat.primary`.|
| Set a default language.|Pass `multiLangChat.primary` with `multiLangChat.supportedLangs`. The primary value must be one of the supported languages included the array.|
| Enable language detection.|Pass `primary: null` or `primary: 'und'` with `multiLangChat`. |
| Dynamically update the chat language. | Call the `setPrimaryChatLanguage(lang)` API.|

### Text-to-Speech

Feature flag: `enableBotAudioResponse: true` (default: `false`)

Default TTS: `WebSDK.TTS.oracle`

Feature configuration: `ttsVoice`

You can enrich the conversational experience by enabling text-to-speech (TTS) to speak the responses as they reach the SDK. The SDK provides two types of TTS service out of the box: `WebSDK.TTS.platform` and `WebSDK.TTS.oracle`. By default, the SDK uses the Oracle Cloud Infrastructure (OCI) Speech service, to have the responses spoken in a more naturalistic tone. This service has several voices that you can select from to provide a more branded experience. However, you can instead use the platform-dependent TTS service, `WebSDK.TTS.platform` that's based on the Web Speech API. It uses the speech synthesis APIs on the user's device to speak the responses.

You use the `ttsVoice` array to configure the voice for the TTS. Each item in the array must be an object that has at least a `lang` field or a `name` field. The SDK looks up the availability of each voice in the order that they are passed in the setting. The first complete match is set as the voice. If no exact match is found, then the SDK uses the first match based on the `lang` value alone. If there's still no match, then the SDK uses the default voice.

```js
var settings = {
    ...,
    enableBotAudioResponse: true,
    ttsVoice: [{
        lang: 'en-US',
        name: 'Samantha'
    }, {
        lang: 'en-US',
        name: 'Alex'
    }, {
        lang: 'en-UK'
    }]
}
```

To tailor the way the utterances are spoken, the `ttsVoice` array allows passing optional `pitch`, `rate`, and `volume` properties in each item. These properties correspond to the same fields in [SpeechSynthesisUtterance](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance) interface.

 * The `pitch` property can have a value between 0 and 2.
 * The `rate` property can have a value between 0.1 and 10.
 * The `volume` property can have a value between 0 and 1.

```js
var settings = {
    // ....,
    ttsVoice: [{
        lang: 'en-us',
        name: 'Alex',
        pitch: 1.5,
        rate: 2,
        volume: 0.8
    }, {
        lang: 'en-us',
        name: 'Victoria',
        pitch: 1.2,
        rate: 1.7,
    }, {
        lang: 'en',
        name: 'Fiona',
        pitch: 2,
    }, {
        lang: 'en'
    }]
}
```

### Speech Synthesis Service Injection

Feature configuration: `ttsService`

By utilizing the device's native text-to-speech service, the SDK's text-to-speech (TTS) synthesis uses the device's service allows the skill's responses to be uttered as soon as they're received by the Web SDK instance. This is the out-of-the-box approach, and while it's reliable, it does have a few drawbacks:

* You're often limited to unnatural, generic-sounding voices that can undermine your branding.
* A user's device may not support gender-specific voices.
* Some native frameworks (Cordova and ReactNative among them) require third-party libraries for TTS services because their webviews do not expose the native `speechSynthesis` APIs that are required by the Web SDK.

To address these challenges, you can set the voice used for the skill's responses by injecting a TTS service into the SDK instance. You can use your own TTS, or one provided by a third-party.

#### Speech Synthesis Service Interface

You need to implement the `SpeechSynthesisService` interface for the TTS service instance that you're going to inject.

```js
/**
 * Interface for the speech synthesis service; this can be used to define a service that can be
 * injected into the SDK to perform speech synthesis on behalf of the skill or assistant
 */
interface SpeechSynthesisService {
    /**
     * Adds a phrase to the utterance queue to be spoken
     * @param phrase string
     */
    speak(phrase: string): void;

    /**
     * Cancels any ongoing speech synthesis utterance
     */
    cancel(): void;

    /**
     * Returns a Promise that resolves into a list of SpeechSynthesisServiceVoice objects representing
     * the available voices
     *
     * @return {*}  {Promise<SpeechSynthesisServiceVoice[]>}
     */
    getVoices(): Promise<SpeechSynthesisServiceVoice[]>;

    /**
     * Sets the voice to be used for speaking the utterances. It accepts an array of candidate voices
     * sorted in their preference order, and sets one of them according to its matching criteria.
     * It returns a Promise that gets resolved when the voice is set.
     *
     * @param {SpeechSynthesisServiceVoice[]} voice
     * @return {*}  {Promise<void>}
     */
    setVoice(voices: SpeechSynthesisServiceVoice[]): Promise<void>;

    /**
     * Returns the voice that is used for speaking the utterances
     */
    getVoice(): SpeechSynthesisServiceVoice;

    /**
     * Adds listener to SpeechSynthesisServiceEvent
     *
     * @param {SpeechSynthesisServiceEvent} event
     * @param {Function} listener
     */
    on(event: SpeechSynthesisServiceEvent, listener: () => void): void;

    /**
     * Removes listener(s) to SpeechSynthesisServiceEvent
     *
     * @param {SpeechSynthesisServiceEvent} event
     * @param {Function} listener
     */
    off(event: SpeechSynthesisServiceEvent, listener?: () => void): void;
}
```

You must implement or extend the `SpeechSynthesisServiceVoice` interface for the voices used in the speech synthesis service:

```js
/**
 * Represents a voice that the SpeechSynthesisService supports. Every SpeechSynthesisServiceVoice has
 * its own relative speech service including information about language, name and optionally more.
 */
interface SpeechSynthesisServiceVoice {
    /**
     * Returns a BCP 47 language tag indicating the language of the voice
     */
    readonly lang: string;

    /**
     * Returns a human-readable name that represents the voice
     */
    readonly name: string;

    /**
     * Pitch of the voice, can range between 0 and 2, default is 1
     * Optional
     */
    pitch?: number;

    /**
     * Speed at which the utterance is spoken at, can range between 0.1 and 10, default is 1
     * Optional
     */
    rate?: number;

    /**
     * Volume at which the utterance is spoken at, can range between 0 and 1, default is 1
     * Optional
     */
    volume?: number;
}
```

The `SpeechSynthesisServiceEvent` object has two events:

```js
const SpeechSynthesisServiceEvent = {
    TTSPlay: 'tts:play',
    TTSEnd: 'tts:end'
}
```

Once your TTS service is mapped to an object that implements the Speech Synthesis API, it can be passed to the SDK for injection of the TTS service. The service can be injected when this object is passed to the `ttsService` field during initialization, or it can be injected dynamically by passing the object to the `setTTSService(service)` method.

After the TTS service has been injected, the SDK handles the calls to the service methods for uttering the messages. However, you can call these methods directly, or you can use the TTS methods exposed by the SDK for any requirement. In headless mode, for example, you can call the `Bots.speakTTS(message)` method to pass a message as it is received from the skill. The SDK handles both the parsing of the utterable text from the message and the passing of this text to the TTS service so that it can be uttered.

### Voice Recognition

Feature flag: `enableSpeech: true` (default: `false`)

Feature configuration: `enableSpeechAutoSend`

The SDK has been integrated with speech recognition to send messages in the form of voice to skills and digital assistants. It allows users to talk directly to the skill during conversations and get appropriate responses.

When the feature is enabled, a mic button appears in place of the send button whenever the user input field is empty. The user can click on the mic button to start the voice recording and send it to the speech server for recognition. The speech is converted to text and sent to the skill or digital assistant. If the speech is partially recognized, the partial result is set in the user input field and the user can clean it up before sending it.

The feature can also be utilized using two exposed methods - `startVoiceRecording(onSpeechRecognition, onSpeechNetworkChange, options)` to start recording, and `stopVoiceRecording()` to stop recording. The APIs are detailed in the Method section above.

The `enableSpeechAutoSend` flag setting lets you configure whether to send the text that's recognized from the user's voice directly to the chat server. When set to `true` (the default), the user's speech response is automatically sent to the chat server. When set to `false`, the user's speech response is rendered in the input text field before it is sent to the chat server so that users can manually modify it before sending or deleting the message.


### Absolute and Relative Timestamps

Feature configuration: `timestampMode`

You can enable absolute or relative timestamps for chat messages. Absolute timestamps display the exact time for each message. Relative timestamps display only on the latest message and express the time in terms of the moments, minutes, hours, days, months, or years ago relative to the previous message.

The precision afforded by absolute timestamps makes them ideal for archival tasks, but within the limited context of a chat session, this precision detracts from the user experience because users must compare timestamps to find out the passage of time between messages. Relative timestamps allow users to track the conversation easily through terms like *Just Now* and *A few moments ago* that can be immediately understood. Relative timestamps improve the user experience in another way while also simplifying your development tasks: because relative timestamps mark the messages in terms of seconds, minutes, hours, days, months, or years ago, you don't need to convert them for time zones.

### Cross-Tab Conversation Synchronization

Feature flag: `enableTabsSync: true` (default: `true`)

You may need to open the website in multiple tabs for various reasons. With `enableTabsSync: true`, you can synchronize and continue your conversation from any tab, as long as the connections parameters (i.e., `URI`, `channelId`, and `userId`) are the same across all tabs. This feature ensures that you can see messages from the skill on any tab and respond from the same tab or any other one.

Additionally, if you clear the conversation history in one tab, it is deleted from other tabs as well. If you update the chat language on one tab, it also gets synchronized on other tabs.

>**Limitations**
* A new tab synchronizes with existing tab(s) for the new messages between you and the skill on opening. If you have not configured the SDK to display messages from your conversation history, the initial chat widget on the new tab will appear empty when opened.
* If you have configured the SDK to display conversation history, the messages from the current chat on existing tabs will appear as part of conversation history on a new tab. If `disablePastActions` is set `'all'` or `'postback'`, you may not be able to interact with the actions of those messages in the new tab.
* The Safari browser currently does not support this feature.

### End Conversation Session

Feature flag: `enableEndConversation: true` (default: `true`)

This feature adds a close button to the chat header that allows user to end the current conversation session. Clicking the close button opens a confirmation prompt. On confirming the action, the SDK sends an event message to the skill to mark the current conversation session as ended. The instance then disconnects from the skill, collapses the chat widget, and erases the conversation history of the current user. It also raises a `'chatend'` event that you can register for. Opening the chat widget afterward starts a new conversation session.

The conversation can also be ended by calling `Bots.endChat()` method. This comes in handy when the SDK is initialised in headless mode.

### Default Client Responses

Feature flag: `enableDefaultClientResponse: true` (default: `false`)

Use this flag to provide default client-side responses along with a typing indicator when the skill response has been delayed, or when there's no skill response at all. If the user sends out the first message/query, but the skill does not respond within the number of seconds set by `defaultGreetingTimeout`, the skill can display a greeting message that's configured using the [defaultGreetingMessage](#custom-text) translation string. Next, the client checks again for the skill response. The client displays the skill response if it has been received, but if it hasn't, then the client displays a wait message (configured with the [defaultWaitMessage](#custom-text) translation string) at intervals set by `defaultWaitMessageInterval`. When the wait for the skill response exceeds the threshold set by `typingIndicatorTimeout`, the client displays a sorry response to the user and stops the typing indicator. You can configure the sorry response using the [defaultSorryMessage](#custom-text) translation string.

### Custom Message Rendering

Feature flag: `delegate.render: (message) => boolean` (default: `undefined`)

This feature lets you override the default message rendering with your custom message template. To use this feature, you need to implement the `render` delegate function which takes the message model as the input and returns a boolean flag as the output. It must return `true` to replace the default rendering with your custom rendering for a particular message type. If `false` is returned, the default message is rendered instead.

> **Note**: For custom rendering, all of the action click handling, and the disabling or enabling of action must be handled explicitly.

You can use any external framework component for your message rendering. Refer to the integration samples to check how you can use this feature with such frameworks like React, Angular and Oracle JavaScript Extension Toolkit (JET).

### Live Agent Typing Indicator

Feature flag: `enableSendTypingStatus: boolean` (default: `false`)

This feature allows agents to ascertain if users are still engaged in the conversation by sending the user status to the live agent. When this flag is enabled, the SDK sends a `RESPONDING` status message with the text that is currently being typed by the user to Oracle Service Cloud. This, in turn, displays a typing indicator on the agent console. When the user has finished typing, the SDK sends a `LISTENING` status message to Oracle Service Cloud to hide the typing indicator on the agent console.

The `typingStatusInterval` configuration, which has a minimum value of three seconds, throttles the typing status update.

To send the agent both the text as it's being typed by the user and the typing status, `enableAgentSneakPreview` (which by default is `false`) must be set to `true` and Sneak Preview must be configured in Oracle Service Cloud. For more details refer to [Sneak Preview documentation](https://docs.oracle.com/en/cloud/saas/service/18a/famug/chat-configuration.html#c_Enabling_Sneak_Preview)

> **Note**: You do not have to configure live typing status on the user side. The user can see the live typing status of the agent by default. When the agent is typing, the SDK receives a `RESPONDING` status message which results in the display of a typing indicator in the user's view. Similarly, when the agent is idle, the SDK receives a `LISTENING` status message which hides the typing indicator.

## Customization

Customizability is one of the biggest strengths of the Web SDK. In this section, we'll cover some of the various customization that can be performed on the SDK.

### Add Avatar Icons to Messages

The messages in the chat are not accompanied by any avatars by default. You can, however, display icons with user and skill messages with the following parameters:
* `avatarBot` - The URL of the image source, or the source string of the SVG image that should be displayed alongside the skill messages.
* `avatarUser` - The URL of the image source, or the source string of the SVG image that should be displayed alongside the user messages.
Additionally, if the skill has a live agent integration, the SDK can be configured to show a different icon for agent messages.
* `avatarAgent` - The URL of the image source or the source string of the SVG image that should be displayed alongside the agent messages. If this value is not provided, but `avatarBot` is set, the `avatarBot` icon is used instead.

```js
new WebSDK({
    URI: '<URI>',
    //...,
    icons: {
        avatarBot: '../assets/images/avatar-bot.png',
        avatarUser: '../assets/images/avatar-user.jpg',
        avatarAgent: '<svg xmlns="http://www.w3.org/2000/svg" height="24" width="24"><path d="M12 6c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2m0 9c2.7 0 5.8 1.29 6 2v1H6v-.99c.2-.72 3.3-2.01 6-2.01m0-11C9.79 4 8 5.79 8 8s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm0 9c-2.67 0-8 1.34-8 4v3h16v-3c0-2.66-5.33-4-8-4z"/></svg>'
    }
})
```

All of the above settings can only be passed in the initialization settings. They cannot be modified dynamically.

### Card Cardinal Utterance for Card Messages

To identify the place of each card in a CRC cards message during a TTS utterance, the `card` translation string is used with its cardinal number before the content of each card. If the cards message contains a single card though, this identifier is skipped.

The default string used for the `card` translation key is `'Card {0}'`, where the placeholder `{0}` is replaced with its cardinal position. You can overwrite this translation with your own custom string. If you do not include the placeholder `{0}` in your custom string, it is added to the end of the string by default. You can localize the string by placing `{0}` before or after the word.

If you don't want this card identifier to be uttered, you can do so by passing an empty string to the `card` key.

```js
i18n: {
    en: {
        card: '',           // Will prevent uttering 'Card 1', 'Card 2' before the card message content
    }
}
```

### Change Header Buttons Icons

There are three buttons on the chat header that be displayed in the chat widget. These buttons can be configured and customized as follows:

* Clear Message button - Clicking this button clears the current and older messages in the conversation.
    * Feature flag - `enableClearMessage: true`
    * Custom icon - `icons.clearHistory: '<image URL | SVG string>'`
* Audio response toggle button - This button toggles the utterance of skill responses as they are received. As it is a toggle button, it has two states, utterance on, where responses are spoken, and utterance off, where responses are not spoken.
    * Feature flag - `enableBotAudioResponse: true`
    * Custom icon - response on - `icons.ttsOn: '<image URL | SVG string>'`
                    response off - `icons.ttsOff: '<image URL | SVG string>'`
* Close widget button - This button collapses the widget and shows the launch button. This button can not be disabled in normal chat widget, and it is not shown in the embedded chat widget.
    * Feature flag - none (always enabled in the chat widget, not displayed in embedded mode)
    * Custom icon - `icons.collapse : '<image URL | SVG string>'`

These header button icons can be customized in two ways: through passing the source URL of the image, or through a raw SVG string. If a raw SVG string is passed, the fill color of the SVG can be customized by CSS classes, as well as by passing a color value in the `colors.headerButtonFill` property in the initial settings. The color customization may not work for all SVGs, as they can be multi-colored or have their own stroke and fill colors.

### Draggable Launch Button and widget

Feature flag: `enableDraggableButton: true` (default: `false`)

Feature flag: `enableDraggableWidget: true` (default: `false`)

In some scenarios, the chat widget or the launch button can block the background content and there may not be an easy way to view it. This can be especially apparent in mobile screens where there is less space available for the web page. However, by setting `enableDraggableButton` or `enableDraggableWidget` to `true`, the chat widget or launch button can be made draggable, so the users can drag it around the screen as needed.

### Feedback Message's Rating Gauge

The new feedback component enables users to rate their interactions with your skill. When users complete a conversation flow, the feedback message presents users with a star rating system, a row of stars (typically there are five stars, depending on the configuration of the `System.Feedback` component in the dialog flow). The stars are highlighted as users hover over them, which indicates that they have selected a rating.

You can change the icon for the component's rating selecting buttons by passing the icon of your choice in using the `rating` icon setting. For the best user experience, use a solid SVG string without a fill color, as it allows for a recognizable highlighting on hover.

```js
new WebSDK({
    URI: '<Server URI>',
    //...,
    icons: {
        rating: '<svg height="24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M15.994 3.006a5.7 5.7 0 00-3.795 1.707L12 4.916l-.199-.202a5.676 5.676 0 00-8.128 0c-2.231 2.275-2.231 5.953 0 8.228L12 21.428l8.326-8.486A5.873 5.873 0 0022 8.828a5.873 5.873 0 00-1.675-4.115A5.693 5.693 0 0016.262 3z"/></svg>'    // A heart icon
    }
})
```

The color of the icon in the two states, unselected and hovered/selected, can be configured with the `ratingStar` and `ratingStarFill` color fields in `colors` setting respectively.

```js
new WebSDK({
    URI: '<Server URI>',
    //...,
    icons: {
        rating: '<svg height="24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M15.994 3.006a5.7 5.7 0 00-3.795 1.707L12 4.916l-.199-.202a5.676 5.676 0 00-8.128 0c-2.231 2.275-2.231 5.953 0 8.228L12 21.428l8.326-8.486A5.873 5.873 0 0022 8.828a5.873 5.873 0 00-1.675-4.115A5.693 5.693 0 0016.262 3z"/></svg>'    // A heart icon
    },
    colors: {
        ratingStar: '#ffebee',
        ratingStarFill: '#d32f2f'
    }
})
```

### Focus First Action of Skill Message

Feature flag: `focusOnNewMessage: 'action'` (default: `'input'`)

With each new message, the chat widget normally sets the focus back to the user input field. This works well when the dialog flow expects a lot of textual input from the user. However, if the dialog flow contains a number of messages with actions, then the user needs to either use their mouse or reverse tab navigation to select one of the actions. For such use cases and for power users who prefer keyboard-based navigation, a better choice can be focusing the first action button in the skill message as it is received. By setting `focusOnNewMessage: 'action'`, when a new skill message containing actions is received, the focus is set to the first action button. If the message does not contain any actions, the focus is set to the user input field.

### Format Message Timestamps

Feature flag: `timestampMode: 'relative' | 'absolute'` (default: `'relative'`)

Functionality configuration: `timestampFormat`

Timestamps are shown with messages indicating the time they were sent or received. By default, they are displayed in the locale time in day of week, month date, year, time am/pm format (Thursday, August 13, 2020, 9:52:22 AM, for example). This timestamp can be configured by passing formatting options in the `timestampFormat` setting.

The formatting can be performed in two ways - by passing a pattern string consisting of formatting tokens, or by passing an object containing [Intl.DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat#Syntax) options.

* Using pattern string
The timestamp can be formatted by passing a pattern string which is composed of format tokens. The available format tokens are:

| Component | Token | Output |
| --------- | ----- | ------ |
| Day of Month | D | 1 2 ... 30 31 |
|| Do | 1st 2nd ... 30th 31st |
|| DD | 01 02 ... 30 31 |
| Day of Week | d | 0 1 ... 5 6 |
|| ddd | Sun Mon ... Fri Sat |
|| dddd | Sunday Monday ... Friday Saturday |
| Month | M | 1 2 ... 11 12 |
|| MM | 01 02 ... 11 12 |
|| MMM | Jan Feb ... Nov Dec |
|| MMMM | January February ... November December |
| Year | YY | 70 71 ... 29 30 |
|| YYYY | 1970 1971 ... 2029 2030 |
| Hour | H | 0 1 ... 22 23 |
|| HH | 00 01 ... 22 23 |
|| h | 1 2 ... 11 12 |
|| hh | 01 02 ... 11 12 |
| Minute | m | 0 1 ... 58 59 |
|| mm | 00 01 ... 58 59 |
| Second | s | 0 1 ... 58 59 |
|| ss | 00 01 ... 58 59 |
| Fractional Second | S | 0 1 ... 8 9 |
|| SS | 0 1 ... 98 99 |
|| SSS | 0 1 ... 998 999 |
|AM/PM | A | AM PM |
|| a | am pm |
| Timezone | Z | -07:00 -06:00 ... +06:00 +07:00 |
|| ZZ | -0700 -0600 ... +0600 +0700 |

So, passing timestampFormat: `'hh:mm:ss a'` would set timestamp as '09:30:14 pm'.

> **Note**: The tokens in the pattern string are case-sensitive: e.g., passing `yyyy` instead of `YYYY` would not display a year in the date.

* Using the `Intl.DateTimeFormat` options object

The timestamp can also be formatted using the options defined for [Intl.DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat#Syntax) object. The object can be passed with some or all of the following properties:

| Property | Acceptable Values |
| -------- | ----------------- |
| `dateStyle` | `'full'`, `'long'`, `'medium'`, `'short'` |
| `timeStyle` | `'full'`, `'long'`, `'medium'`, `'short'` |
| `weekday` | `'long'` (e.g., Thursday), `'short'` (e.g., Thu), `'narrow'` (e.g., T) |
| `day` | `'numeric'` (e.g., 1), `'2-digit'` (e.g., 01) |
| `month` | `'numeric'` (e.g., 2), `'2-digit'` (e.g., 02), `'long'` (e.g., March), `'short'` (e.g., Mar), `'narrow'` (e.g., M) |
| `year` | `'numeric'` (e.g., 2012), `'2-digit'` (e.g., 12) |
| `era` | `'long'` (e.g., Anno Domini), `'short'` (e.g., AD), `'narrow'` (e.g., A) |
| `hour` | `'numeric'`, `'2-digit'` |
| `minute` | `'numeric'`, `'2-digit'` |
| `second` | `'numeric'`, `'2-digit'` |
| `timeZoneName` |  `'long'` (e.g., British Summer Time), `'short'` (e.g., GMT+1) |
| `timeZone` | The time zone to use. The only value implementations must recognize is "UTC"; the default is the runtime's default time zone. Implementations may also recognize the time zone names of the IANA time zone database, such as "Asia/Shanghai", "Asia/Kolkata", "America/New_York". |
| `hour12` | Whether to use 12-hour time (as opposed to 24-hour time). Possible values are `true` and `false` |

### Open Links

Custom handling: `linkHandler: { onclick: <function>, target: '<string>' }`

In the In-widget Webview : `linkHandler: { target: 'oda-chat-webview' }`

In new window: `openLinksInNewWindow: true`

The Web SDK provides various ways for you to control the target location of the URL links within the conversations. By default, clicking any link in the conversation opens the linked URL in the new tab. You can configure the widget to open it in a specific target using `linkHandler` setting.

The `linkHandler` setting expects an object that can take two optional fields - `target` and `onclick`. The `target` field accepts a string that identifies the location where the linked URL is to be displayed (a tab, window, or \<iframe\>). The following keywords have special meanings for where to load the URL:
* `'_self'`: the current browsing context.
* `'_blank'`: usually a new tab, but users can configure browsers to open a new window instead.
* `'_parent'`: the parent browsing context of the current one. If no parent, behaves as `'_self'`.
* `'_top'`: the topmost browsing context (the "highest" context that’s an ancestor of the current one). If no ancestors, behaves as `'_self'`.

```js
settings = {
    ...,
    linkHandler: { target: '_blank'}
};

var Bots = new WebSDK(settings);
```

To open the links inside an `iframe`, you can pass its name attribute in the `target` property.

```html
<iframe name="container" width="400" height="300"></iframe>

<script>
  settings = {
      ...
      linkHandler: { target: 'container'}
  }

  var Bots = new WebSDK(settings);
</script>
```

The `onclick` property of `linkHandler` allows you to add an event listener on all anchor links in the conversation. The listener is fired before the link is opened, and can be used to perform actions based on the link. The listener is passed an `event` object as parameter that is generated by the click action. You can prevent the link from being opened by returning `false` from the listener. The listener is also bound to the anchor element that is clicked, and the `this` context refers to the `HTMLAnchorElement` inside the listener.

```js
linkHandler: {
    onclick: function(event) {
        console.log('The element clicked is', this);
        console.log('The event fired from the click is', event);
        console.log('The clicked link is', event.target.href);
        console.log('Preventing the link from being opened');
        return false;
    }
}
```
You can set either one or both properties of the `linkHandler` setting, but passing one of the fields is required.

In some scenarios, you may want to open links explicitly in a new window, overriding browser preferences. This can be achieved by passing `openLinksInNewWindow: true` in the settings.

Finally, the chat widget also provides an in-widget Webview that can be used to display linked URLs inside the widget. This helps in preventing the user from navigating away from the page to a new tab or window. See [In-Widget Webview](#in-widget-webview) for more details on this feature.

### Relative Timestamps

Feature flag: `timestampMode: 'relative'`

Timestamp color: `colors.timestamp: 'color string'`

The appearance of the message timestamps can be modified with the `timestampMode` setting. When set as `'relative'`, the timestamp is only shown before the first message of the day as a header, and for the new messages as an updating timestamp indicating the time passed since the message was added in the conversation. This relative timestamp is refreshed in the following intervals if no new message is added:
* For the first 10s
* Between 10s-60s
* Every minute between 1m-60m
* Every hour between 1hr-24hr
* Every day between 1d-30d
* Every month between 1m-12m
* Every year after the first year

As soon as a new message is added to the conversation, the relative timestamp from the last message is removed and added to the new message. The timestamp is also updated to start afresh for the new message.

For older messages in the conversation, a timestamp header is shown indicating the date before the first message of the day, for all days a conversation is performed. The timestamp header format can be customized using the `timestampFormat` setting.

### Restrict Attachment Types

`Feature flag: enableAttachment: true` (default: `true`)

`Functionality configuration: shareMenuItems`

Users can share various kinds of files and their location to the skills using the share menu from the chat widget. By default, the share attachment popup menu shows 4 items - sharing visual media files (i.e., images and videos, audio files, general files like documents, PDF, excel sheets, etc., and location). This menu can be customized to show fewer options using the `shareMenuItems` setting. This setting accepts an array of strings where each item maps to a menu item – `'visual'` for **Share Image/Video**, `'audio'` for **Share Audio**, `'file'` for **Share File**, and `'location'` for **Share Location**. The share menu only shows the items for passed values, so by passing fewer items, the share menu can be modified. For example, passing `shareMenuItems: ['audio', 'location']` in the settings will only show the `Share Audio` and `Share Location` menu items in the share popup menu. However, passing an empty array, or invalid values will show all menu items. To show no items, the feature can be disabled by passing `enableAttachment: false`.

#### Custom Share Menu Items

Starting with Version 21.04, you can configure the share menu items to set specific file types that users are allowed to upload. The custom menu item can be passed as an object to the `shareMenuItems` array. It can be passed along with the string categories, or can also be passed without them. A custom share menu item may look as follows:
```js
{
    type: string,       // Space separated list of file formats, pass '*' to allow all supported filie types

    label: string,      // OPTIONAL, label for the share menu item, should preferably be configured through i18n strings

    icon?: string,      // OPTIONAL, Icon image source path or SVG source string, the file icon is displayed as fallback

    maxSize?: number    // OPTIONAL, Maximum file size allowed for upload in KiloBytes, the maximum and fallback value is 25 MB (25600 KB)
}
```

The following code snippet shows passing custom menu items in settings and defining their labels using the `i18n` field.

```js
var settings = {
    shareMenuItems: [ {
        type: 'odf',
        label: 'Upload ODF',
    }, {
        type: 'pdf'
    }, {
        type: 'jpg png jpeg',
        icon: 'https://image-source-site/imageicon'
    }, {
        type: 'doc docx xls',
        maxSize: 4096
    }],
    i18n: {
        en: {
            share_pdf: 'Upload PDF',
            share_jpg_png_jpeg: 'Upload Image',
            share_doc_docx_xls: 'Upload document'
        }
    }
}
```
As illustrated by the above snippet, the `i18n` labels for the custom menu items can be set by passing them with `share_\<type joined by '_'\>` keys. For the wildcard `'*'`, the label can be set using the `'share_all'` `i18n` key. Using `i18n` is recommended over the `label` as it allows supporting the menu item labels in multiple languages.

Using attachment functionality often requires updating the network security policy of the host site. The attachments are uploaded to ODA object storage using HTTP calls and may get blocked by the site's [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) policies. With the site blocking the uploads, an error can be seen in the browser console indicating that the client has blocked the request due to CORS policy. To fix such issues, the network security policy of the host site should be updated to whitelist the ODA domain, allowing the upload requests to go through.
Since the CORS policy does not apply to WebSockets, the conversations between the SDK and ODA skills are not impacted by such restrictions.

When connecting to a client auth enabled channel on the ODA platform running Version 20.12 and above, you can optionally make attachments more secure by passing `enableAttachmentSecurity: true`. When set to `true`, extra headers are passed to the attachment upload requests to ensure that they can't be downloaded without passing a valid signed JWT token as the value of the `token` query parameter in the attachment fetch request URL.

> **Note**: Do not enable this setting if the skill connects to an ODA instance that's Version 20.08 or runs on any Version prior to 20.08. This property only applies to client auth-enabled connections to Versions 20.12 and higher of the ODA platform.


## Message Model

To use features like headless mode and delegate, a clear understanding of skill and user messages is essential. Everything received from and sent to the chat server are represented as messages. This includes:
* Messages from the user to the skill (e.g., "I want to order a Pizza")
* Messages from the skill to the user (e.g., "What kind of crust do you want?")

The following section describes each of the message types in more detail.

### Base Types
These are the base types that are used by user-to-skill messages and skill-to-user messages. They are the building blocks for the messages.


#### Action
An action represents something that the user can select. Every action includes the following properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The action type | string | Yes |
| `label` | The descriptive label text for the action. | string | At least a single `label` or `imageUrl` property must be present |
| `imageUrl` | Image to display for the action | string | At least a single `label` or `imageUrl` property must be present. |
| `style` | The rendering style of the button | `"primary"`, `"danger"`, `"default"` | No |
| `displayType` | The rendering for the type of action element (button, link, or icon). | `"button"`, `"link"`, `"icon"` | No |
| `channelExtensions` | The channel-specific extension properties associated with the action | JSONObject | No |


##### PostbackAction
This action will send a predefined postback back to the skill if the user selects the action.
It adds the following properties to the `Action` properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The action type | `"postback"` | Yes |
| `postback` | The postback to be sent back if the action is selected | string or JSONObject | Yes |

Example JSON
```json
{
    "type": "postback",
    "label": "Large Pizza",
    "imageUrl": "https://amicis.com/images/gallery/locations/11.jpg",
    "postback": {
        "state": "askSize",
        "action": "getCrust"
    }
}
```


##### CallAction
This action will request the client to call a specified phone number on the user's behalf.
It adds the following properties to the `Action` properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The action type | `"call"` | Yes |
| `phoneNumber` | The phone number to call | string | Yes |

Example JSON
```json
{
    "type": "call",
    "label": "Call Support",
    "imageUrl": "http://ahoraescuando.bluefm.com.ar/files/2016/05/cuidado.jpg",
    "phoneNumber": "18002231711"
}
```


##### UrlAction
This action will request the client to open a website in a new tab or in an in-app browser.
It adds the following properties to the `Action` properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The action type | `"url"` | Yes |
| `URL` | The URL of the website to display | string | Yes |


##### ShareAction
This action will request the client to open a sharing dialog for the user.
It adds the following properties to the `Action` properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The action type | `"share"` | Yes |


##### LocationAction
This action will request the client to ask the user for a location.
It adds the following properties to the `Action` properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The action type | `"location"` | Yes |

Example JSON
```json
{
    "type": "location",
    "label": "Share location",
    "imageUrl": "http://images.clipartpanda.com/location-clipart-location-pin-clipart-1.jpg"
}
```


##### SubmitFormAction

This action is used to submit an Editable Form to the skill in case the form passes the client side validation.
It adds the following properties to the `Action` properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The action type | `"submitForm"` | Yes |
| `postback` | The postback payload, which might include an action property to trigger navigation. The value of this property should be set in the [FormSubmissionMessagePayload](#user-form-submission-message) | JSONObject | No |

Example JSON
```json
{
    "type": "submitForm",
    "label": "Submit",
    "postback": {
        "system.botId": "6803DE12-DAA9-4182-BD54-3B4D431554F4",
        "system.flow": "ExpenseFlow",
        "system.state": "editFormMapVar"
    }
}
```


##### PopupAction

This action opens a pop-up window after users perform a click action on an element. `PopupAction` uses the `Action` properties along with its own:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The action type | `"popup"` | Yes |
| `popupContent` | The content that displays within the pop-up window. | The message payload (refer to the following JSON example) | Yes |

Example JSON
```json
{
    "type": "popup",
    "label": "Give Feedback",
    "popupContent": {
        "formRows": [
            {
                "columns": [
                    {
                        "width": "stretch",
                        "fields": [
                            {
                                "displayType": "text",
                                "label": "What was the issue with this response?"
                            },
                            {
                                "displayType": "multiSelect",
                                "options": [
                                    {
                                        "label": "Inaccurate",
                                        "value": "inaccurate"
                                    },
                                    {
                                        "label": "Inappropriate",
                                        "value": "inappropriate"
                                    }
                                ],
                                "id": "system_feedback_reasons",
                                "required": true
                            },
                            {
                                "displayType": "textInput",
                                "id": "system_feedback_comments",
                                "placeholder": "Additional feedback"
                            }
                        ]
                    }
                ]
            },
            {
                "columns": [
                    {
                        "fields": [
                            {
                                "displayType": "action",
                                "action": {
                                    "postback": {
                                        "rating": "negative",
                                        "action": "cancel",
                                    },
                                    "label": "Cancel",
                                    "type": "postback"
                                },
                            }
                        ]
                    },
                    {
                        "fields": [
                            {
                                "displayType": "action",
                                "action": {
                                    "postback": {
                                        "rating": "negative",
                                        "system.state": "invokeLLM"
                                    },
                                    "label": "Submit Feedback",
                                    "type": "submitForm"
                                },
                            }
                        ]
                    }
                ]
            }
        ],
        "type": "editForm",
        "title": "Give your feedback",
        "formColumns": 1,
    }
}
```


#### Attachment
This represents an attachment that's sent from the user to the skill or from the skill to the user.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `title` | A title for the attachment | string | No |
| `type` | The type of attachment | `"audio"`, `"file"`, `"image"`, `"video"` | Yes |
| `URL` | The URL to download the attachment | string | Yes |

Example JSON
```json
{
    "title": "Oracle Open World Promotion",
    "type": "image",
    "URL": "https://www.oracle.com/us/assets/hp07-oow17-promo-02-3737849.jpg"
}
```


#### Card
A card represents a single card in the message payload.  It contains the following properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `title` | The title of the card, displayed as the first line on the card. | string | Yes |
| `description` | The description of the card | string | No |
| `imageUrl` | URL of the image that is displayed | string | No |
| `URL` | URL of a website that is opened when taping on the card | string | No |
| `actions` | An array of actions related to the text | Array\<Action\> | No |
| `channelExtensions` | The channel-specific extension properties associated with the card | JSONObject | No |


#### Location
This represents a Location object.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `title` | A title for the location | string | No |
| `URL` | A URL for displaying a map of the location | string | No |
| `latitude` | The GPS coordinate's longitude value | double | Yes |
| `longitude` | The GPS coordinate's longitude value | double | Yes |

Example JSON
```json
{
    "title": "Oracle Headquarters",
    "URL": "https://www.google.com.au/maps/place/37°31'47.3%22N+122°15'57.6%22W",
    "longitude": -122.265987,
    "latitude": 37.529818
}
```

#### Heading

This represents a heading for tables in a `Table` or `Table-Form` object.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `label` | The label for the heading | string | Yes |
| `alignment` | Positioning of the label within its cell | `"left"`, `"right"`, `"center"` | Yes |
| `width` | Suggested percentage of table width that should be provided to the heading | number | No |
| `channelExtensions` | The channel-specific extension properties associated with the heading | JSONObject | No |

#### Field

This represents the atomic information of a table cell or a form field in `Table`, `Form`, and `Table-Form` object, provided as key-value pair.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | string | Yes |
| `label` | Key of the field | string | No |
| `marginTop` | The amount of vertical space between this field and the previous field in the same column | `"none"`, `"medium"`, `"large"` | No |
| `labelFontSize` | The font size used for the field label | `"small"`, `"medium"`, `"large"` | No |
| `labelFontWeight` | The font weight used for the field label | `"light"`, `"medium"`, `"bold"` | No |
| `channelExtensions` | The channel-specific extension properties associated with the field | JSONObject | No |

#### SelectFieldOption

The SingleSelect and MultiSelect fields use a list of select options with following properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `label` | The display text | string | Yes |
| `value` | The raw value for the choice | Primitive data types (string, number, boolean, etc.) | Yes |
| `channelExtensions` | The channel-specific extension properties associated with the field option | JSONObject | No |

#### Read Only Field

This represents a read only field. All read only fields inherit the generic field properties and have the following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `value` | The field value | string | No |
| `alignment` | The positioning of the label within its cell. | `"left"`, `"right"`, `"center"` | No |
| `width` | The suggested percentage of the total available width that the field should occupy in a table layout. | number | No |

##### Text Field

The text field inherits all read only field properties and has following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"text"` | Yes |
| `truncateAt` | The position at which lengthy text gets truncated and an ellipsis mark (which indicates the value has been truncated) displays. | number | No |
| `fontSize` | The font size used for the field value | `"small"`, `"medium"`, `"large"` | No |
| `fontWeight` | The font weight used for the field value | `"light"`, `"medium"`, `"bold"` | No |

##### Link Field

The link field inherits all read only field properties and has following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"link"` | Yes |
| `linkLabel` | The label used for the hyperlink | string | No |
| `imageUrl` | The URL of the image that opens a link when clicked. | string | No |

> **Note**: If both `linkLabel` and `imageUrl` are present, image will be displayed that opens a link when clicked.

##### Media Field

The media field inherits all read only field properties and has following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"media"` | Yes |
| `mediaType` | The field media type. | `"video"`, `"audio"`, `"image"` | Yes |

##### Action Field

The media field inherits all read only field properties and has following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"action"` | Yes |
| `action` | The action that should be performed when the user clicks the action button. | `Action` | Yes |

#### Editable Field

This represents an editable field. All editable fields inherit the generic field properties and have the following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `id` | The ID of the field | string | Yes |
| `placeholder` | A description of the input that's expected from the user. This text displays when the user has not yet made a selection or entered a value. | string | No |
| `required` | Whether this input is required | boolean | No |
| `clientErrorMessage` | The field level error message that's displayed below the field when a client-side validation error occurs. If not provided, SDK defaults to `editFieldErrorMessage` | string | No |
| `serverErrorMessage` | The field level error message that's displayed below the field when a server-side validation error occurs. This error message must be included in the payload sent by the skill. | string | No |
| `autoSubmit` | When set to true, the form is partially submitted when the user has entered a value for the field. See [Auto-Submit](#auto-submit) for more details. | boolean | No |

##### SingleSelect

The single select field inherits all editable field properties and has the following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"singleSelect"` | Yes |
| `defaultValue` | The default selection | Primitive data types (string, number, boolean, etc.) | No |
| `options` | An array of options presented to the user. | Array\<[SelectFieldOption](#selectfieldoption)\> | Yes |
| `layoutStyle` | The layout style used to render the single select options. The default layout is `list`. | `"list"`, `"radioGroup"` | No |

##### MultiSelect

The multi select field inherits all editable field properties and has the following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"multiSelect"` | Yes |
| `defaultValue` | The default selection | Array\<object\> primitive data types (could be a string, number, boolean, etc.) | No |
| `options` | An array of options presented to the user. | Array\<[SelectFieldOption](#selectfieldoption)\> | Yes |
| `layoutStyle` | The layout style used to render the multi select options. The default layout is `list`. | `"list"`, `"checkboxes"` | No |

##### DatePicker

The date picker field inherits all editable field properties and has the following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"datePicker"` | Yes |
| `defaultValue` | The initial value for this field, format must be YYYY-MM-DD | string | No |
| `minDate` | The minimum, or earliest, date allowed. The format must be YYYY-MM-DD. | string | No |
| `maxDate` | The maximum, or latest, date allowed. The format must be YYYY-MM-DD. | string | No |

##### TimePicker

The time picker field inherits all editable field properties and has the following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"timePicker"` | Yes |
| `defaultValue` | The initial value for this field, format must be HH:mm in 24H format | string | No |
| `minTime` | The minimum, or earliest, time allowed, entered as HH:mm in 24-hour format. For example, 00:00. | string | No |
| `maxTime` | The maximum, or latest, time allowed, entered as HH:mm in 24-hour format. For example, 00:00. | string | No |

##### Toggle

The toggle field inherits all editable field properties and has the following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"toggle"` | Yes |
| `defaultValue` | The initial selected value. If you want the toggle to be initially on, set this to the value of  `valueOn`'s value. | string | No |
| `valueOff` | The value when toggle is off | string | Yes |
| `valueOn` | The value when toggle is on | string | Yes |
| `labelOff` | The label that is displayed when the toggle field is hovered in the off state | string | No |
| `labelOn` | The label that is displayed when the toggle field is hovered in the on state | string | No |

##### TextInput

The text input field inherits all editable field properties and has the following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"textInput"` | Yes |
| `defaultValue` | The initial value for this field | string | No |
| `validationRegularExpression` | A regular expression indicating the required format for this text input | string | No |
| `multiline` | The flag that determines whether to render multiple lines of input | boolean | No |
| `minLength` | The minimum length of input that the user must provide | number | No |
| `maxLength` | The maximum number of characters allowed in the text input field | number | No |
| `inputStyle` | The input style that should be rendered that fallbacks to `text` when not specified. Allowable values are: `"text"`, `"tel"`, `"url"`, `"email"` and `"password"` | string | No |

##### NumberInput

The number input field inherits all editable field properties and has the following additional properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `displayType` | The field type | `"numberInput"` | Yes |
| `defaultValue` | The initial value for this field | number | No |
| `minValue` | A smallest allowable number | number | No |
| `maxValue` | A largest allowable number | number | No |

#### Row

This represents an array of fields.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `fields` | Array of fields | Array\<Field\> | Yes |
| `selectAction` | The action that is executed when the row is selected. The label of the action is shown as a tooltip when users hover over the row. | `Action` | No |
| `channelExtensions` | The channel-specific extension properties associated with the row | JSONObject | No |

#### Form

This represents an array of fields or form rows along with a title. Used in `Table-Form` messages for nested forms of a table row.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `id` | The ID of the form | string | No |
| `title` | A representative title for the form in the table row | string | No |
| `fields` | Array of fields | Array\<Field\> | Yes |
| `formRows` | A list of rows displayed in the form. You can define either the list of fields using the `fields` property, or a list of rows using this property. The `fields` and `formRows` properties are mutually exclusive. | Array\<FormRow\> | No |
| `selectAction` | The action that is executed when the form is selected. The label of the action is shown as a tooltip when users hover over the form. | `Action` | No |
| `actions` | A list of actions displayed at the bottom of the form | Array\<Action\> | No |
| `channelExtensions` | The channel-specific extension properties associated with the form | JSONObject | No |

#### FormRow

A form row contains a list of columns that are laid out side-by-side. Multiple form rows are laid out vertically with each form row starting on a new line below the previous form row.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `id` | The ID of the form row | string | No |
| `columns` | A list of columns displayed in the form row | Array\<Column\> | No |
| `selectAction` | The action that is executed when the form row is selected. The label of the action is shown as a tooltip when users hover over the form row. | `Action` | No |
| `separator` | When set to `true`, a separator line is added above the form row content | boolean | No |
| `channelExtensions` | The channel-specific extension properties associated with the form row | JSONObject | No |

#### Column

A column contains a list of fields. These fields are laid out vertically.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `id` | The ID of the column | string | No |
| `fields` | A list of fields displayed vertically in the column. The fields must be [read only fields](#read-only-field) when the column is used in a [FormRow](#formrow) within a [Form message](#skill-form-message). The fields can include both editable and read only fields when the [FormRow](#formrow) is used within an [Edit-Form message](#skill-edit-form-message). | Array\<Field\> | Yes |
| `verticalAlignment` | The vertical alignment of the column with respect to other columns in the same form row | string | No |
| `width` | Property that determines how the width of the column is determined within the form row | `"auto"`, `"stretch"` | No |
| `channelExtensions` | The channel-specific extension properties associated with the column | JSONObject | No |

#### PaginationInfo

This represents the paging information of results in a `Table`, `Form`, and `Table-Form` object.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `totalCount` | Total count of results | number | Yes |
| `rangeSize` | Range size of results per page | number | Yes |
| `status` | Paging status message | string | Yes |
| `currentRangeSize` | Size of curent range of results | number | Yes |
| `rangeStart` | Starting offset of the current range of results | number | Yes |
| `nextRangeSize` | Size of the next range of results | number | Yes |
| `hasPrevious` | Indicates whether there is a previous set of results | boolean | Yes |
| `hasNext` | Indicates whether there is next set of results | boolean | Yes |

#### EventContextProperties

The Event Context Properties represent the CloudEvent context properties.

| Name | Description | Type | Required? | Example |
| ------ | ------ | ------ | ------ | ------ |
| `dataschema` | Identifies the schema that the data adheres to. | URI | No | `"/dw/approval_payload.json"` |
| `datacontenttype` | The content type of the data contained in the data attribute. | string | No | `"application/json" `|
| `source` | The resource that produced the event. | URI | No | `"objectstorage"` |
| `time` | The time of the event expressed in RFC 3339 timestamp format. | Timestamp | No | `"2021-01-10T21:19:24Z"` |
| `specversion` | The version of the CloudEvents specification | string | No | `"1.0"` |
| `id` | The ID of the CloudEvents specification | string | No | `"123e4567-e89b-12d3-a456-426614174000"` |
| `subject` | The event's subject in the context of the event producer and/or event type. | string | No | `"mynewfile.jpg"` |


### Conversation Messages
All messages that are part of the conversation are structured as follows:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `messagePayload` | Message payload | Message | Yes |
| `userId` | User ID | string | Yes |

Example conversation message
```json
{
    "messagePayload": {
        "text": "show menu",
        "type": "text"
    },
    "userId": "guest"
}
```


### Message
Message is the abstract base type for all other messages. All messages extend it to provide more information.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | string | Yes |


### User Message
This represents a [Message](#message-1) sent from a user to a skill.


#### User Text Message
This is a simple text message sent to the server.
It applies the following properties to the `Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"text"` | Yes |
| `text` | Text message | string | Yes |

```json
{
    "messagePayload": {
        "text": "Order Pizza",
        "type": "text"
    },
    "userId": "guest"
}
```


#### User Attachment Message
This is the attachment response message sent to the server.
It applies the following properties to the `Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"attachment"` | Yes |
| `attachment` | Attachment metadata | Attachment | Yes |

```json
{
    "messagePayload": {
        "attachment": {
            "type": "image",
            "URL": "http://oda-instance.com/attachment/v1/attachments/d43fd051-02cf-4c62-a422-313979eb9d55"
        },
        "type": "attachment"
    },
    "userId": "guest"
}
```


#### User Location Message
This is the location response message sent to the server.
It applies the following properties to the `Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"location"` | Yes |
| `location` | User location information | Location | Yes |

```json
{
    "messagePayload": {
        "location": {
            "latitude": 45.9285271,
            "longitude": 132.6101925
        },
        "type": "location"
    },
    "userId": "guest"
}
```


#### User Postback Message
This is the postback response message sent to the server.
It applies the following properties to the `Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"postback"` | Yes |
| `text` | Text for postback | string | No |
| `postback` | The postback of the selected action | string or JSONObject | Yes |

```json
{
    "messagePayload": {
        "postback": {
            "variables": {
                "pizza": "Small"
            },
            "system.botId": "69F2D6BB-35BF-4BCA-99A0-A88D44A51B35",
            "system.state": "orderPizza"
        },
        "text": "Small",
        "type": "postback"
    },
    "userId": "guest"
}
```

#### User InboundEvent Message
This represents the inbound event messages that can be sent to the server.
It applies the following properties to the `Message`

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"inboundEvent"` | Yes |
| `eventType` | The event type (defined in the event catalog) | string | Yes |
| `eventVersion` | The event type version (defined in the event catalog) | string | Yes |
| `eventData` | The business data | JSONObject | Yes |
| `contextProperties` | The event context properties | EventContextProperties | No |

Here's an example:

```json
{
    "messagePayload": {
        "eventData": {
            "size": "Medium",
            "type": "Cheese"
        },
        "eventVersion": "1.0",
        "eventType": "com.pizzastore.pizza.orderserved",
        "type": "inboundEvent",
        "contextProperties": {
            "id": "6ce23f09-bff7-4369-8467-0c510e971aaf",
            "source": "pizza/service",
        }
    },
    "userId": "guest"
}
```

#### User Form Submission Message
This represents the form submission message that's sent after the user has submitted a form by clicking [SubmitFormAction](#submitformaction). It has the following properties:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"formSubmission"` | Yes |
| `submittedFields` | Key-value pairs of the submitted field values. The key is the name (ID) of the field. | JSONObject | Yes |
| `postback` | The postback payload, which might include an action property to trigger navigation. The value of this property should be taken from the [SubmitFormAction](#submitformaction) | JSONObject | No |
| `partialSubmitField` | The ID of the field that triggers a partial form submission. Fields with the `autoSubmit` property set to `true` can trigger a partial form submission. See [Auto-Submit](#auto-submit) for more details. | string | No |

Here's an example:

```json
{
    "messagePayload": {
        "submittedFields": {
            "Attendees": [
                "Toff van Alphen"
            ],
            "Type": "Public transport",
            "Description": "expense",
            "Subject": "Expense",
            "Date": "2023-06-07",
            "Time": "18:58",
            "Amount": 6,
            "TipIncluded": "true"
        },
        "partialSubmitField": "Attendees",
        "type": "formSubmission"
    },
    "userId": "guest"
}
```

### Skill Message
This represents a [Message](#message-1) sent from a skill to a user.
It applies the following properties to the `Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | string | Yes |
| `headerText` | The header text displayed above the message text | string | No |
| `footerText` | The footer text displayed below the message text and actions, but before the global actions | string | No |
| `actions` | A list of actions related to the message | Array\<Action\> | No |
| `footerForm` | A form layout that displays below the footer text of the message and above its global actions. | [Form](#form) | No |
| `globalActions` | A list of global actions related to the text | Array\<Action\> | No |
| `channelExtensions` | The channel-specific extension properties associated with the message | JSONObject | No |


#### Skill Text Message
This represents a text message.
It applies the following properties to the `Skill Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"text"` | Yes |
| `text` | Text of the message | string | Yes |


```json
{
    "messagePayload": {
        "type": "text",
        "text": "What do you want to do?",
        "actions": [
            {
                "type": "postback",
                "label": "Order Pizza",
                "postback": {
                    "state": "askAction",
                    "action": "orderPizza"
                }
            },
            {
                "type": "postback",
                "label": "Cancel A Previous Order",
                "postback": {
                    "state": "askAction",
                    "action": "cancelOrder"
                }
            }
        ]
    },
    "userId": "guest"
}
```


#### Skill Attachment Message
This represents an attachment message.
It applies the following properties to the `Skill Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"attachment"` | Yes |
|`attachment` | The attachment sent | Attachment | Yes |


#### Skill Location Message
This represents a location message.
It applies the following properties to the `Skill Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"location"` | Yes |
| `location` | The location | Location | Yes |


#### Skill Postback Message
This represents a postback.
It applies the following properties to the `Skill Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"postback"` | Yes |
| `text` | Text of the message | string | No |
| `postback` | The postback | string or JSONObject | Yes |


#### Skill Card Message
This represents a set of choices displayed to the user, either horizontally like a carousal or vertically like a list.
It applies the following properties to the `Skill Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"card"` | Yes |
| `layout` | Whether to display the cards horizontally or vertically | string (values: horizontal, vertical) | Yes |
| `cards` | Array of cards to be rendered | Array\<Card\> | Yes |

Example JSON
```json
{
    "messagePayload": {
        "type": "card",
        "layout": "horizontal",
        "cards": [
            {
                "title": "Hawaiian Pizza",
                "description": "Ham and pineapple on thin crust",
                "actions": [
                    {
                        "type": "postback",
                        "label": "Order Small",
                        "postback": {
                            "state": "GetOrder",
                            "variables": {
                                "pizzaType": "hawaiian",
                                "pizzaCrust": "thin",
                                "pizzaSize": "small"
                            }
                        }
                    },
                    {
                        "type": "postback",
                        "label": "Order Large",
                        "postback": {
                            "state": "GetOrder",
                            "variables": {
                                "pizzaType": "hawaiian",
                                "pizzaCrust": "thin",
                                "pizzaSize": "large"
                            }
                        }
                    }
                ]
            },
            {
                "title": "Cheese Pizza",
                "description": "Cheese pizza (i.e. pizza with NO toppings) on thick crust",
                "actions": [
                    {
                        "type": "postback",
                        "label": "Order Small",
                        "postback": {
                            "state": "GetOrder",
                            "variables": {
                                "pizzaType": "cheese",
                                "pizzaCrust": "thick",
                                "pizzaSize": "small"
                            }
                        }
                    },
                    {
                        "type": "postback",
                        "label": "Order Large",
                        "postback": {
                            "state": "GetOrder",
                            "variables": {
                                "pizzaType": "cheese",
                                "pizzaCrust": "thick",
                                "pizzaSize": "large"
                            }
                        }
                    }
                ]
            }
        ],
        "globalActions": [
            {
                "type": "call",
                "label": "Call for Help",
                "phoneNumber": "123456789"
            }
        ]
    },
    "userId": "guest"
}
```


#### Skill Feedback Message
This represents a feedback rating component that takes user's feedback using a rating gauge. Typically, this gauge is represented as a star rating system. Its payload is similar to a normal text message, but it has an additional `channelExtensions` object field that is set as `{ "displayType": "stars" }`.
It applies the following properties to the `Skill Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"text"` | Yes |
| `text` | Text of the message | string | Yes |
| `channelExtensions` | An object depicting specific extension to the payload | `{ "displayType": "stars" }` | Yes |

Example JSON
```json
{
    "messagePayload":{
        "text":"How would you like to rate us?",
        "type":"text",
        "actions":[
            {
                "postback":{
                    "variables":{
                        "rating":"1"
                    },
                    "system.botId":"61C8D800-23AF-4DDD-B5AF-D79AB3F3BE67",
                    "action":"1",
                    "system.state":"giveFeedback"
                },
                "label":"1",
                "type":"postback"
            },
            {
                "postback":{
                    "variables":{
                        "rating":"2"
                    },
                    "system.botId":"61C8D800-23AF-4DDD-B5AF-D79AB3F3BE67",
                    "action":"2",
                    "system.state":"giveFeedback"
                },
                "label":"2",
                "type":"postback"
            },
            {
                "postback":{
                    "variables":{
                        "rating":"3"
                    },
                    "system.botId":"61C8D800-23AF-4DDD-B5AF-D79AB3F3BE67",
                    "action":"3",
                    "system.state":"giveFeedback"
                },
                "label":"3",
                "type":"postback"
            },
            {
                "postback":{
                    "variables":{
                        "rating":"4"
                    },
                    "system.botId":"61C8D800-23AF-4DDD-B5AF-D79AB3F3BE67",
                    "action":"4",
                    "system.state":"giveFeedback"
                },
                "label":"4",
                "type":"postback"
            },
            {
                "postback":{
                    "variables":{
                        "rating":"5"
                    },
                    "system.botId":"61C8D800-23AF-4DDD-B5AF-D79AB3F3BE67",
                    "action":"5",
                    "system.state":"giveFeedback"
                },
                "label":"5",
                "type":"postback"
            }
        ],
        "channelExtensions":{
            "displayType":"stars"
        }
    },
    "source":"BOT",
    "userId":"<userID>"
}
```


#### Skill Table Message
Represents a message that returns the results of a query in table form The message consists of an array of headings and an array of rows. The rows themselves contain a `fields` array that represents individual cells.
It applies the following properties to the `Skill Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"table"` | Yes |
| `headings` | An array of table headings  | Array\<Heading\> | Yes |
| `rows` | An array of table rows. Each row contains a `fields` array that represents the table cells. | Array\<Row\> | Yes |
| `tableTitle` | The table title | string | No |
| `paginationInfo` | The paging information for the results in the table | `PaginationInfo` | No |

Example JSON
```json
{
    "type":"table",
    "headerText":"A-Team",
    "tableTitle": "Document",
    "headings":[
        {
            "width":20,
            "label":"First Name",
            "alignment":"left"
        },
        {
            "width":20,
            "label":"Last Name",
            "alignment":"left"
        },
        {
            "width":35,
            "label":"Title",
            "alignment":"left"
        },
        {
            "width":25,
            "label":"Phone",
            "alignment":"right"
        }
    ],
    "rows":[
        {
            "fields":[
                {
                    "displayType":"text",
                    "width":20,
                    "label":"First Name",
                    "alignment":"left",
                    "value":"Aaron"
                },
                {
                    "displayType":"text",
                    "width":20,
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Adams"
                },
                {
                    "displayType":"text",
                    "width":35,
                    "label":"Title",
                    "alignment":"left",
                    "value":"Demo Builder"
                },
                {
                    "displayType":"text",
                    "width":25,
                    "label":"Phone",
                    "alignment":"right",
                    "value":"1234567890"
                }
            ]
        },
        {
            "fields":[
                {
                    "displayType":"text",
                    "width":20,
                    "label":"First Name",
                    "alignment":"left",
                    "value":"Bob"
                },
                {
                    "displayType":"text",
                    "width":20,
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Brown"
                },
                {
                    "displayType":"text",
                    "width":35,
                    "label":"Title",
                    "alignment":"left",
                    "value":"Multi-lingual Expert"
                },
                {
                    "displayType":"text",
                    "width":25,
                    "label":"Phone",
                    "alignment":"right",
                    "value":"1234567890"
                }
            ]
        },
        {
            "fields":[
                {
                    "displayType":"text",
                    "width":20,
                    "label":"First Name",
                    "alignment":"left",
                    "value":"Charlie"
                },
                {
                    "displayType":"text",
                    "width":20,
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Chase"
                },
                {
                    "displayType":"text",
                    "width":35,
                    "label":"Title",
                    "alignment":"left",
                    "value":"Flow Builder"
                },
                {
                    "displayType":"text",
                    "width":25,
                    "label":"Phone",
                    "alignment":"right",
                    "value":"1234567890"
                }
            ]
        },
        {
            "fields":[
                {
                    "displayType":"text",
                    "width":20,
                    "label":"First Name",
                    "alignment":"left",
                    "value":"David"
                },
                {
                    "displayType":"text",
                    "width":20,
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Davidson"
                },
                {
                    "displayType":"text",
                    "width":35,
                    "label":"Title",
                    "alignment":"left",
                    "value":"Machine Learning Expert"
                },
                {
                    "displayType":"text",
                    "width":25,
                    "label":"Phone",
                    "alignment":"right",
                    "value":"1234567890"
                }
            ]
        },
        {
            "fields":[
                {
                    "displayType":"text",
                    "width":20,
                    "label":"First Name",
                    "alignment":"left",
                    "value":"Eric"
                },
                {
                    "displayType":"text",
                    "width":20,
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Eastman Junior"
                },
                {
                    "displayType":"text",
                    "width":35,
                    "label":"Title",
                    "alignment":"left",
                    "value":"Docker Expert"
                },
                {
                    "displayType":"text",
                    "width":25,
                    "label":"Phone",
                    "alignment":"right",
                    "value":"1234567890"
                }
            ]
        }
    ],
    "paginationInfo":{
        "currentRangeSize":5,
        "rangeStart":0,
        "nextRangeSize":-3,
        "hasPrevious":false,
        "hasNext":false,
        "totalCount":5,
        "rangeSize":8,
        "status":"Showing 1-5 of 5 items"
    }
}
```


#### Skill Form Message
Represents a message that returns the results of a query in a form that's read only. The message consists of an array of form results. Each form result contains a `fields` array with key-value pairs that represent a field.
It applies the following properties to the `Skill Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"form"` | Yes |
| `forms` | An array of form results. Each result contains a fields array that represents the `form` fields. | Array\<Row\> | Yes |
| `formColumns` | A number suggesting the number of columns in which the fields of the form should be grouped. | 1, 2 | Yes |
| `paginationInfo` | The paging information for the results in the form | `PaginationInfo` | No |

Example JSON
```json
{
    "type":"form",
    "headerText":"A-Team",
    "forms":[
        {
            "fields":[
                {
                    "displayType":"text",
                    "label":"First Name",
                    "alignment":"left",
                    "value":"Aaron"
                },
                {
                    "displayType":"text",
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Adams"
                },
                {
                    "displayType":"text",
                    "label":"Title",
                    "alignment":"left",
                    "value":"Demo Builder"
                },
                {
                    "displayType":"text",
                    "label":"Phone",
                    "alignment":"left",
                    "value":"1234567890"
                },
                {
                    "linkLabel":"Open Link",
                    "displayType":"link",
                    "label":"Contact",
                    "alignment":"left",
                    "value":"https://www.example.com/in/aaron-adams-4862752"
                },
                {
                    "displayType":"text",
                    "label":"Bio",
                    "alignment":"left"
                }
            ]
        },
        {
            "fields":[
                {
                    "displayType":"text",
                    "label":"First Name",
                    "alignment":"left",
                    "value":"Bob"
                },
                {
                    "displayType":"text",
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Brown"
                },
                {
                    "displayType":"text",
                    "label":"Title",
                    "alignment":"left",
                    "value":"Multi-lingual Expert"
                },
                {
                    "displayType":"text",
                    "label":"Phone",
                    "alignment":"left",
                    "value":"1234567890"
                },
                {
                    "linkLabel":"Open Link",
                    "displayType":"link",
                    "label":"Contact",
                    "alignment":"left",
                    "value":"https://www.example.com/in/Bobbrown"
                },
                {
                    "displayType":"text",
                    "label":"Bio",
                    "alignment":"left",
                    "value":"Bob is a member of the cloud architects team which is specialized in enterprise mobility and cloud development. Bob has been directly involved with Oracle middleware since 2005 during which he held different roles in managing highly specialized teams."
                }
            ]
        },
        {
            "fields":[
                {
                    "displayType":"text",
                    "label":"First Name",
                    "alignment":"left",
                    "value":"Charlie"
                },
                {
                    "displayType":"text",
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Chase"
                },
                {
                    "displayType":"text",
                    "label":"Title",
                    "alignment":"left",
                    "value":"Flow Builder"
                },
                {
                    "displayType":"text",
                    "label":"Phone",
                    "alignment":"left",
                    "value":"1234567890"
                },
                {
                    "linkLabel":"Open Link",
                    "displayType":"link",
                    "label":"Contact",
                    "alignment":"left",
                    "value":"https://www.example.com/in/Charlie-chase-97a418"
                },
                {
                    "displayType":"text",
                    "label":"Bio",
                    "alignment":"left",
                    "value":"Charlie is a member of the enterprise mobility team. Charlie has 20+ years experience with custom development. Charlie is an expert on mobile cloud services and development tools. He is the creator of productivity tools. His latest passion is building chatbots with a minimum amount of custom code."
                }
            ]
        }
    ],
    "formColumns":2,
    "paginationInfo":{
        "currentRangeSize":3,
        "rangeStart":0,
        "nextRangeSize":2,
        "hasPrevious":false,
        "hasNext":true,
        "totalCount":5,
        "rangeSize":3,
        "status":"Showing 1-3 of 5 items"
    },
    "globalActions":[
        {
            "postback":{
                "variables":{},
                "action":"system.showMore"
            },
            "label":"Show More",
            "type":"postback"
        }
    ]
}
```


#### Skill Table-Form Message
This message combines the `Table` and `Form` message types. It represents a message that returns the results of a query in the form of a table. Each each row of the table has a read-only form in addition to the row information.
It applies the following properties to the `Skill Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"tableForm"` | Yes |
| `headings` | An array of table headings  | Array\<Heading\> | Yes |
| `rows` | An array of table rows each themselves containing an array of fields representing the table cells | Array\<Row\> | Yes |
| `forms` | An array of form results that correspond to each table row. Each form contains a `fields` array that represents the form fields. | Array\<Form\> | Yes |
| `formColumns` | The number suggesting the number of columns in which the fields of the form should be grouped. | 1, 2 | Yes |
| `tableTitle` | The table title | string | No |
| `paginationInfo` | The paging information for the results in the table form | `PaginationInfo` | No |

Example JSON
```json
{
    "type":"tableForm",
    "headerText":"A-Team",
    "tableTitle":"Document",
    "headings":[
        {
            "width":47,
            "label":"First Name",
            "alignment":"left"
        },
        {
            "width":47,
            "label":"Last Name",
            "alignment":"left"
        }
    ],
    "rows":[
        {
            "fields":[
                {
                    "displayType":"text",
                    "label":"First Name",
                    "alignment":"left",
                    "value":"Aaron"
                },
                {
                    "displayType":"text",
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Adams"
                }
            ]
        },
        {
            "fields":[
                {
                    "displayType":"text",
                    "label":"First Name",
                    "alignment":"left",
                    "value":"Bob"
                },
                {
                    "displayType":"text",
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Brown"
                }
            ]
        },
        {
            "fields":[
                {
                    "displayType":"text",
                    "label":"First Name",
                    "alignment":"left",
                    "value":"Charlie"
                },
                {
                    "displayType":"text",
                    "label":"Last Name",
                    "alignment":"left",
                    "value":"Chase"
                }
            ]
        }
    ],
    "forms":[
        {
            "title":"View details Aaron Adams",
            "fields":[
                {
                    "displayType":"text",
                    "label":"Title",
                    "alignment":"left",
                    "value":"Demo Builder"
                },
                {
                    "displayType":"text",
                    "label":"Phone",
                    "alignment":"left",
                    "value":"1234567890"
                },
                {
                    "linkLabel":"Open Link",
                    "displayType":"link",
                    "label":"Contact",
                    "alignment":"left",
                    "value":"https://www.example.com/in/Aaron-adams-4862572"
                },
                {
                    "displayType":"text",
                    "label":"Bio",
                    "alignment":"left"
                }
            ]
        },
        {
            "title":"View details Bob Brown",
            "fields":[
                {
                    "displayType":"text",
                    "label":"Title",
                    "alignment":"left",
                    "value":"Multi-lingual Expert"
                },
                {
                    "displayType":"text",
                    "label":"Phone",
                    "alignment":"left",
                    "value":"1234567890"
                },
                {
                    "linkLabel":"Open Link",
                    "displayType":"link",
                    "label":"Contact",
                    "alignment":"left",
                    "value":"https://www.example.com/in/Bobbrown"
                },
                {
                    "displayType":"text",
                    "label":"Bio",
                    "alignment":"left",
                    "value":"Bob is a member of the cloud architects team which is specialized in enterprise mobility and cloud development. Bob has been directly involved with Oracle middleware since 2005 during which he held different roles in managing highly specialized teams."
                }
            ]
        },
        {
            "title":"View details Charlie Chase",
            "fields":[
                {
                    "displayType":"text",
                    "label":"Title",
                    "alignment":"left",
                    "value":"Flow Builder Fanatic"
                },
                {
                    "displayType":"text",
                    "label":"Phone",
                    "alignment":"left",
                    "value":"1234567890"
                },
                {
                    "linkLabel":"Open Link",
                    "displayType":"link",
                    "label":"Contact",
                    "alignment":"left",
                    "value":"https://www.example.com/in/Charlie-chase-97a418"
                },
                {
                    "displayType":"text",
                    "label":"Bio",
                    "alignment":"left",
                    "value":"Charlie is a member of the enterprise mobility team. Charlie has 20+ years experience with custom development. Charlie is an expert on mobile cloud services and development tools. He is the creator of productivity tools. His latest passion is building chatbots with a minimum amount of custom code."
                }
            ]
        }
    ],
    "formColumns":2,
    "paginationInfo":{
        "currentRangeSize":3,
        "rangeStart":0,
        "nextRangeSize":2,
        "hasPrevious":false,
        "hasNext":true,
        "totalCount":5,
        "rangeSize":3,
        "status":"Showing 1-3 of 5 items"
    },
    "actions":[
        {
            "postback":{
                "variables":{

                },
                "action":"system.showMore"
            },
            "label":"Show More",
            "type":"postback"
        }
    ],
    "footerText":"Tap on a row to see personal details"
}
```


#### Skill Edit-Form Message
Represents an Editable Form message. The message consists of an array of `fields`.

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type. | `"editForm"` | Yes |
| `title` | A representative title for the edit form | string | No |
| `fields` | A list of fields which can include both editable and read only fields. | Array\<Field\> | Yes |
| `formRows` | A list of rows which can include both editable and read only fields. You can define either the list of fields (using the `fields` and optionally, the `formColumns` properties), or a list of rows using this property. The `fields` and `formRows` properties are mutually exclusive. | Array\<FormRow\> | No |
| `formColumns` | The number of columns in which the form fields should be grouped. Only applicable when `fields` property is set. | number | Yes |
| `errorMessage` | A form-level error message that displays when the user has submitted invalid data but the error cannot be linked to an individual field. | string | No |
| `actions` | An array of actions related to the edit form. This array should include a `SubmitFormAction`. An error displays in the browser console when the `SubmitFormAction` is not included in the actions array.  | Array\<Action\> | No |
| `globalActions` | An array of global actions | Array\<Action\> | No |
| `channelExtensions` | A set of channel-specific extension properties. The `channelExtensions` object can include a `replaceMessage` property that's used to replace the previous Edit-Form message. See [Replacing Previous Edit-Form](#replacing-previous-edit-form) section for more details on this feature. | JSONObject | No |

Here's an example:

Example JSON
```json
{
    "messagePayload": {
        "headerText": "Create Expense",
        "type": "editForm",
        "title": "Fill in the below form",
        "fields": [
            {
                "displayType": "textInput",
                "serverErrorMessage": "Invalid Text Input",
                "defaultValue": "Expense",
                "minLength": 5,
                "id": "Subject",
                "label": "Subject",
                "placeholder": "Enter subject of the expense",
                "clientErrorMessage": "Subject is required and must be between 5 and 15 characters",
                "maxLength": 15,
                "required": true
            },
            {
                "displayType": "textInput",
                "defaultValue": "expense",
                "multiLine": true,
                "id": "Description",
                "label": "Description",
                "placeholder": "What is expense justification",
                "clientErrorMessage": "Description is required",
                "required": true
            },
            {
                "displayType": "datePicker",
                "defaultValue": "2023-06-07",
                "maxDate": "2023-06-22",
                "id": "Date",
                "label": "Expense Date",
                "placeholder": "Pick a date in the past",
                "clientErrorMessage": "Expense date is required and must be in the past.",
                "required": true
            },
            {
                "displayType": "timePicker",
                "defaultValue": "18:58",
                "id": "Time",
                "label": "Expense Time",
                "placeholder": "What time was the expense",
                "clientErrorMessage": "Time is required. Please fill a value",
                "required": true
            },
            {
                "displayType": "numberInput",
                "minValue": 5,
                "defaultValue": 6,
                "maxValue": 500,
                "id": "Amount",
                "label": "Amount",
                "placeholder": "Enter expense amount",
                "clientErrorMessage": "Amount is required and must be between 5 and 500.",
                "required": true
            },
            {
                "autoSubmit": true,
                "displayType": "toggle",
                "defaultValue": "true",
                "labelOn": "Yes",
                "id": "TipIncluded",
                "label": "Tip Included?",
                "valueOff": "false",
                "labelOff": "No",
                "valueOn": "true"
            },
            {
                "displayType": "singleSelect",
                "serverErrorMessage": "Invalid Selection",
                "defaultValue": "Public transport",
                "options": [
                    {
                        "label": "Public transport",
                        "value": "Public transport"
                    },
                    {
                        "label": "Flight",
                        "value": "Flight"
                    }
                ],
                "layoutStyle": "list",
                "id": "Type",
                "label": "Expense Type",
                "placeholder": "Select expense type",
                "clientErrorMessage": "Expense type is required",
                "required": true
            },
            {
                "displayType": "multiSelect",
                "defaultValue": [
                    "Toff van Alphen"
                ],
                "options": [
                    {
                        "label": "Toff van Alphen",
                        "value": "Toff van Alphen"
                    },
                    {
                        "label": "Roger Federer",
                        "value": "Roger Federer"
                    }
                ],
                "layoutStyle": "checkboxes",
                "id": "Attendees",
                "label": "Attendees",
                "placeholder": "Select attendees",
                "clientErrorMessage": "Please select atleast one attendee",
                "required": true
            }
        ],
        "formColumns": 1,
        "actions": [
            {
                "postback": {
                    "system.botId": "6803DE12-DAA9-4182-BD54-3B4D431554F4",
                    "system.flow": "ExpenseFlow",
                    "system.state": "editFormMapVar"
                },
                "label": "Submit",
                "type": "submitForm"
            }
        ],
        "channelExtensions": {
            "replaceMessage": "True"
        }
    },
    "source": "BOT",
    "userId": "guest"
}
```

#### Skill OutboundEvent Message
This represents the outbound event messages that can be sent by the server.
It applies the following properties to the `Message`

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"outboundEvent"` | Yes |
| `eventType` | The event type (defined in the event catalog) | string | Yes |
| `eventVersion` | The event type version (defined in the event catalog) | string | Yes |
| `eventData` | The business data | JSONObject | Yes |
| `contextProperties` | The event context properties | EventContextProperties | No |

Here's an example:

```json
{
    "messagePayload": {
        "eventData": {
            "size": "Medium",
            "type": "Cheese"
        },
        "eventVersion": "1.0",
        "eventType": "com.pizzastore.pizza.ordercreated",
        "type": "outboundEvent",
        "contextProperties": {
            "tenancy": "odaserviceinstance00",
            "specversion": "1.0",
            "id": "7a923f09-bff7-4369-8467-0c510e971aaf",
            "source": "hello/app",
            "time": 1659357000,
            "type": "com.pizzastore.pizza.ordercreated",
            "channelname": "System_Global_Test",
            "version": "1.0",
            "userid": "3910088",
            "contenttype": "application/json"
        }
    }
}
```


#### Skill Raw Message
This is used when a component creates the channel-specific payload itself.
It applies the following properties to the `Message`:

| Name | Description | Type | Required? |
| ------ | ------ | ------ | ------ |
| `type` | The message type | `"raw"` | Yes |
| `payload` | The channel-specific payload | JSONObject | Yes |


## Limitations

There are a few limitations on the usage of the current Web SDK.

* The skills may start sending incorrect messages if the network goes offline for a short time during a chat (such as 10 seconds) before going back online. This only happens when the server response is lost due to a network failure. In such cases, the user may have to send the previous message again or may need to start the conversation afresh. The skill can be designed to handle such cases.
* The attachment file size is limited to 25 MB. Larger files cannot be uploaded in this release.
* The SDK currently only supports a single connection to the ODA instance per userId per browser or device. If multiple connections are made using the same userId from several devices, or multiple browsers on a single device, then only the responses from the skill and digital assistant will be synchronized on all clients, not the user messages.
