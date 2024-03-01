from django import forms

from exchanges.models import CommentXExchangesItems


class CustomSelectWidget(forms.Select):
    def __init__(self, attrs=None):
        extra_css_classes = attrs.get("class", "") + " custom-select-widget"
        attrs["class"] = extra_css_classes.strip()
        super().__init__(attrs)


class CommentXExchangesItemsForm(forms.ModelForm):
    class Meta:
        model = CommentXExchangesItems
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["exchange_item_id"].widget = CustomSelectWidget()
