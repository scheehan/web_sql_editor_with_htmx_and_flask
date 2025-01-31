![submit form](/app/images/intro.png)

# HTMX hx-prompt and hx-confirm underlying implementation with Flask

When its comes to getting user attention on something important before a changes commit. 
Normal way to ensure users are alerted to potential errors or mistakes before they commit changes were with a pop up window message to be prompt after clicked submit button to prevent unintended actions, to get user attention if any error or mistake observed, now is the best time to revert or cancel the submission.  

One of a common method is to use javascript. However, sometime things can gets complicated when uses javescript to achieve what you would like to do. 

For instance, here is 2 simple [javascript snippets example][3] to demonstrate javascript can provide useful internal functions to help build necessary confirmation alert with 
the existing internal functions create a confirmation alert before a form submission.

## Conbine return and confirm methor 
```html
<form onsubmit="return confirm('Do you really want to submit the form?');">
    <input type="submit" />
<form>
```

```javascript
document.getElementById("myForm").addEventListener("submit", function(event) {
    if (!confirm("Are you sure you want to submit this form?")) {
        event.preventDefault();
    }
});
```

However, when its come to intergrade and work together with your web application, it can get pretty complicated once its involve validation and acknowledgement checks.
Here's an integrate additional logic example that includes a basic validation,
Integrates these snippets into your web application can indeed get complicated, especially when dealing with various validation rules and user acknowledgment checks. However, breaking down the logic into smaller, manageable functions can help simplify the process.

## Function with Method and Action

```html
<script>
function validate(form) {

    // validation code here ...

    if(!valid) {
        alert('Please correct the errors in the form!');
        return false;
    }
    else {
        return confirm('Do you really want to submit the form?');
    }
}
</script>
<form onsubmit="return validate(this);">
```

```javascript
document.getElementById("myForm").addEventListener("submit", function(event) {
    let isValid = validateForm(); // Assume validateForm is a function that returns true if the form is valid
    if (!isValid) {
        alert("Please correct the errors in the form before submitting.");
        event.preventDefault();
    } else if (!confirm("Are you sure you want to submit this form?")) {
        event.preventDefault();
    }
});

function validateForm() {
    // Add your validation logic here
    // Return true if the form is valid, otherwise return false
    return true; // Placeholder
}
```
## Advantage of addapting HTMX 

htmx allow us to access modern browser features directly from HTTP 
requests from a set of HTML attributes to simplify many tasks, including issuing AJAX requests.
in this article we are going to walk through both hx-confirm and hx-prompt.  
  
I put up a simple web app SQL editor to demonstrate how hx-confirm and hx-prompt works.
in this article, going to share some insight about underline machanism works to provide more information for how we can take advantage and intergrades into our web application.

![submit form](/app/images/sql_web_page.png)

# Acknowledgement prompt

hx-confirm basically allow us to trigger an event to include original request with 
if you would like to proceed hit OK button, otherwise cancel. similar to what javascript confirm method offered.

As Jinja can be uses as part of the message body, allow us to dynamically show the data information within message body. To me that is a very cool features, as i doesn't need to create a separate javascript function to capture form and retrieve formdata.

in regards to hx-confirm documentation, you may refer to [hx-confirm link][1] for more info. here is a simple demo how it works.

hx-confirm

![hx-confirm](/app/images/hx-confirm-01.gif)

The hx-confirm attribute allows you to confirm an action before issuing a request. This can be useful in cases where the action is destructive and you want to ensure that the user really wants to do it.

```html
<button hx-post='{{ url_for( "delete", number=row[0] ) }}' hx-confirm="Are you sure you wish to delete record name {{ row[1] }}?" hx-target="body">DELETE</button>
```

Let break it down each htmx attribtues.

hx-port used to trigger a HTTP POST request use Jinja flask url_for function to complile intended url to be send to server for processing. As highlighted in image, it allows to dynamically complile with pathname delete together with the record id return from sql DB query.

> hx-post='{{ url_for( "delete", number=row[0] ) }}'

![hx-confirm](/app/images/hx-post-url_HTTP_post_request.png)

In regards to how htmx behavior, when button fire a mouse click event, htmx will trigger event together with confirm function to halt the POST action, waiting for user acknowledgement action whether the user click "OK" or "Cancel" selection. as highlighted with red circle in image below. 

Whereby, "OK" selection will continue to send HTTP POST data to server, and "Cancel" selection will drop the HTTP POST data immediately by click handler. as highlighted with green circle in image below. 

![hx-confirm](/app/images/hx-post-confirm-action-console-event-debug.png)

# Confirmation prompt with inputbox

## hx-prompt

[hx-prompt][2] basically allow us to prompt a pop up window to request user to input certain acknowledgement message before submit changes, and acknowledgement message need to match intended message in order to pass acknowledgement check.

when the acknowledgement message doesn't match, changes will be ignored. exhibit below demonstrate a sql record entry being edit and then submitted by clicking a "UPDATE" button, 
once fired button action, hx-confirm triggered and a window prompt pop up reqest user to input confirmation message. user needs to input intended message as display in message window. user click "ok" button 
to acknowledge the change. form data and HTTP header hx-prompt togerther with input message sent to server.

![hx-confirm](/app/images/hx-prompt-debug-01.gif)

```html
<form hx-prompt="Enter Yes/No to confirm update" hx-post='{{ url_for( "edit", number=edit[0] ) }}' hx-target="body">
```

The hx-prompt attribute allows you to show a prompt together with string message before issuing a request. 
The value of the prompt inputbox will be included in the request in the HX-Prompt header.

htmx:beforeprocessNode and htmx:afterprocessNode event is triggered before and after htmx initializes a DOM node. 
This gives extensions and other external code the ability to modify the contents of a DOM node before it is processed. to add additional features onto a node.
once user input confirmation message and click button "OK" or "Cancel", submit handler will kick in to proceed sent form data to server, which includes HTTP header added with Hx-Prompt message input by user


![hx-confirm](/app/images/hx-prompt-console-log-y-02.png)

![hx-confirm](/app/images/hx-prompt-console-log-y-header-01.png)

```python
        if request.headers['HX-Prompt'] == 'Yes':

            cur.execute('UPDATE users SET username = ?, ext = ?, email = ?'
                            ' WHERE id = ?',
                            (item_name, item_ext, item_email, item_id))
            conn.commit()

```

## Final thoughts:

Under the hood, [htmx][4] uses standard HTML attributes to trigger JavaScript functions 
that handle the AJAX requests and dialogs. This approach keeps your HTML clean and declarative, while still providing powerful functionality.

By using hx-confirm and hx-prompt, you can easily add user interaction features to 
your web application without writing complex JavaScript code. This can help improve the user experience and reduce the likelihood of errors.

This simple SQL web app were meant to use as demonstration purposes, by no mean cover all use cases.
interested to download and try code sample, please proceed to github repository to download code sample.

### Additional note about htmx debug

Sometime we do need to check debug information for whatever reason. [hx-ext][5] example page got you covered. After install and include debug extension, we need to turn on Verbose level under All levels dropdown menu in browser's developer tools in order to see logs trace.

![hx-debug](/app/images/hx-etx-debug.png)

#### Install under HTML head section

```html
https://unpkg.com/browse/htmx.org@2.0.4/dist/ext/debug.js
```

#### Include into interested HTML mothod

```html
<button hx-post='{{ url_for( "delete", number=row[0] ) }}' hx-target="body" hx-ext="debug">DELETE</button>
```


## Where to download code Sample

### Install & run web app

``` 
git clone https://github.com/scheehan/web_sql_editor_with_htmx_and_flask.git
```
```
cd web_sql_editor_with_htmx_and_flask
pip install -r requirements.txt
```

```
flask run --debug
```


[1]: https://htmx.org/attributes/hx-confirm/
[2]: https://htmx.org/attributes/hx-prompt/
[3]: https://stackoverflow.com/questions/6515502/javascript-form-submit-confirm-or-cancel-submission-dialog-box
[4]: https://htmx.org/docs/#introduction
[5]: https://v1.htmx.org/extensions/debug/
