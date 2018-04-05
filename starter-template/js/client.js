function test() {
    // Define the database object
    var db = firebase.database();

    // Get all of the in
    var input_name = document.getElementById('name').value;
    var input_email = document.getElementById('email').value;
    var input_shortDescription = document.getElementById('shortDescription').value

    var newPostKey = db.ref().child('hello').push().key;
    var data_obj = {
        name: input_name,
        email: input_email,
        desc: input_shortDescription,
        prediction: "NULL",
        actual: "NULL",
        resolved: false
    };
    db.ref().child('tickets').child(newPostKey).update(data_obj).then(function () {
        M.toast({html: 'Your ticket has been submitted successfully. We will get back to you as soon'})

        document.getElementById('name').value = "";
        document.getElementById('email').value = "";
        document.getElementById('shortDescription').value = ""
    });

    event.preventDefault();
    return false
}
