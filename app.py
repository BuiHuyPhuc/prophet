import os
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flask import request, render_template, flash, redirect, url_for
import prophet_util
import config
import validations as val

app = config.create_app(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload():
    if 'upload' not in request.files:
        flash('No file uploaded', 'danger')
        return redirect(url_for('index'))

    file = request.files['upload']
    if file and config.allowed_file(file.filename):
        filepath = get_filepath(file)
        file.save(filepath)
        app.config['UPLOADED_FILE'] = filepath
        validations = val.validate_csv(filepath)
        if not validations:
            prophet_util.create_plots(filepath)
            return redirect(url_for('show'))
        else:
            put_validation_flash(validations)
            return redirect(url_for('index'))

    else:
        flash('Error: wrong extension', 'danger')
        return redirect(url_for('index'))

@app.route('/show', methods=['GET'])
def show():
    return render_template('show.html')

@app.route('/show', methods=['POST'])
def show_custom_prophet():
    txtFuture_periods = request.form.get('txtFuture_periods')
    txtChangepoints = request.form.get('txtChangepoints')
    txtChangepoint_range = request.form.get('txtChangepoint_range')
    txtChangepoint_scale = request.form.get('txtChangepoint_scale')
    ckbCountry_holidays = request.form.get('ckbCountry_holidays')
    txtHolidays_scale = request.form.get('txtHolidays_scale')
    ckbMonthly_seasonality = request.form.get('ckbMonthly_seasonality')
    txtSeasonality_days = request.form.get('txtSeasonality_days')
    txtFourier_monthly = request.form.get('txtFourier_monthly')
    if app.config['UPLOADED_FILE'] != '' and int(txtFuture_periods) > 0 and int(txtChangepoints) > 0 and float(txtChangepoint_range) > 0 and float(txtChangepoint_scale) > 0 and float(txtHolidays_scale) > 0 and float(txtSeasonality_days) > 0 and int(txtFourier_monthly) > 0:        
        prophet_util.custom_plots(app.config['UPLOADED_FILE'], txtFuture_periods, txtChangepoints, txtChangepoint_range, txtChangepoint_scale, ckbCountry_holidays, txtHolidays_scale, ckbMonthly_seasonality, txtSeasonality_days, txtFourier_monthly)
        return redirect(url_for('show'))
    else:
        flash('Error: wrong extension', 'danger')
        return False

def put_validation_flash(validations):
    if not validations:
        flash('File Uploaded', 'success')
    else:
        [flash(err, 'danger') for err in validations]

def get_filepath(file):
    filename = secure_filename(file.filename)
    return os.path.join(app.config['UPLOAD_DIR'], filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
