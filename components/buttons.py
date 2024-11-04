"""

"""

from django_viewcomponent import component

@component.register("button")
class BaseButton(component.Component):
    classlist = ["btn", "ft-black", "bd-radius-2", "bd-width-0", "ft-weight-500"]
    classnames = " ".join(classlist)
    template = """
        <button type="{{ self.type }}" class="{{ self.classnames }} {{ self.extra_css }}">
            {{ self.content }}
        </button>
    """

    variant_map = {
        "primary": "bg-sky-400",
        "secondary": "bg-slate-500",
        "danger": "bg-red-400",
        "warning": "bg-amber-400",
        "success": "bg-emerald-400",
        "info": "bg-blue-400",
    }

    size_map = {
        "sm": "btn-sm",
        "md": "btn-md",
        "lg": "btn-lg",
        "xl": "btn-xl",
        "xxl": "btn-xxl"
    }

    def __init__(
        self, type="button", size="md", variant="primary", **kwargs
        ):
        self.variant = variant
        self.size = size
        self.extra_css = kwargs.get("extra_css", "")
        self.content = kwargs.get("content", "")
        
        if self.variant and self.variant in self.variant_map:
            self.extra_css += f" {self.variant_map[self.variant]}"

        # append css class to the extra_css
        if size and size in self.size_map:
            self.extra_css += f" {self.size_map[size]}"
