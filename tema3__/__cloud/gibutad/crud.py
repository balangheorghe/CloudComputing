# Copyright 2015 Google Inc.
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

from gibutad import get_model, oauth2, storage
from flask import Blueprint, current_app, redirect, render_template, request, \
    session, url_for


crud = Blueprint('crud', __name__)

@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    jobs, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        jobs=jobs,
        next_page_token=next_page_token)


# [START list_mine]
@crud.route("/mine")
@oauth2.required
def list_mine():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    jobs, next_page_token = get_model().list_by_user(
        user_id=session['profile']['id'],
        cursor=token)

    return render_template(
        "list.html",
        jobs=jobs,
        next_page_token=next_page_token)
# [END list_mine]


@crud.route('/<id>')
def view(id):
    job = get_model().read(id)
    return render_template("view.html", job=job)


def upload_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url



# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        file_url = upload_file(request.files.get('details_file'))

        if file_url:
            data['fileURL'] = file_url


        # If the user is logged in, associate their profile with the new job.
        if 'profile' in session:
            data['createdBy'] = session['profile']['displayName']
            data['createdById'] = session['profile']['id']

        job = get_model().create(data)

        return redirect(url_for('.view', id=job['id']))

    return render_template("form.html", action="Add", job={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    job = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        file_url = upload_file(request.files.get('details_file'))

        if file_url:
            data['fileURL'] = file_url

        job = get_model().update(data, id)

        return redirect(url_for('.view', id=job['id']))

    return render_template("form.html", action="Edit", job=job)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
