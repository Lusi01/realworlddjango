def update_fields_widget(form, fields, css_class):
    for field in fields:
        form.fields[field].widget.attrs.update({'class': css_class})

