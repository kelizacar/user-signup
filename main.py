#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

param = {'username_given':"", 'email_given':"", 'error_username': "", 'error_password': "", 'error_verify': "", 'error_email': ""}

short_term_storage = ['nothing']  #holds the username for later

def build_page(errors):

    username ="<label> Username: </label>"
    username_input = "<input type='text' name='username' value = '%s'/>" % param['username_given'] + errors['error_username']

    password ="<label> Password: </label>"
    password_input = "<input type='text' name='password'/>" + errors['error_password']

    ver_password ="<label> Verify Password: </label>"
    ver_password_input = "<input type='text' name='ver_password'/>" + errors['error_verify']

    email ="<label> Email (optional): </label>"
    email_input = "<input type='text' name='email' value = '%s'/>" % param['email_given'] + errors['error_email']

    submit = "<input type='submit' value= 'Sign me up!'/>"

    form = ("<form method='post'>"
            + username + username_input + "<br>"
            + password + password_input + "<br>"
            + ver_password + ver_password_input + "<br>"
            + email + email_input + "<br>"
            + submit +
            "</form>")

    header= "<h2> Signup </h2>"

    return header + form


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{6,20}$")
def valid_username(username_input):
    short_term_storage[0] = username_input
    return username_input and USER_RE.match(username_input)

PASS_RE = re.compile(r"^.{6,20}$")
def valid_password(password_input):
    return password_input and PASS_RE.match(password_input)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email_input):
    return not email_input or EMAIL_RE.match(email_input)

class MainHandler(webapp2.RequestHandler):

    def get(self):

        content = build_page(param)
        self.response.write(content)

    def post(self):
        username_submitted = self.request.get("username")
        password_submitted = self.request.get("password")
        password_ver_submitted = self.request.get("ver_password")
        email_submitted = self.request.get("email")

        have_error = False
        param['error_username'] = ""
        param['error_password'] = ""
        param['error_verify'] = ""
        param['error_email'] = ""
        param['email_given'] = email_submitted
        param['username_given'] = username_submitted

        if not valid_username(username_submitted):
            param['error_username'] = "That is not a valid username. Usernames must be between 6 and 20 characters."
            param['username_given'] = username_submitted
            have_error = True

        if not valid_password(password_submitted):
            param['error_password'] = "That is not a valid password. Passwords must be between 6 and 20 characters."
            have_error= True
        elif password_submitted != password_ver_submitted:
            param['error_verify'] = "Your passwords do not match."
            have_error= True

        if not valid_email(email_submitted):
            param['error_email'] = "That is not a valid email."
            param['email_given'] = email_submitted
            have_error= True

        if have_error:
            self.response.write(build_page(param))
        else: self.redirect('/welcome')



class Welcome(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome, ' + short_term_storage[0])

app = webapp2.WSGIApplication([
                                ('/', MainHandler),
                                ('/welcome', Welcome)],
                              debug=True)
