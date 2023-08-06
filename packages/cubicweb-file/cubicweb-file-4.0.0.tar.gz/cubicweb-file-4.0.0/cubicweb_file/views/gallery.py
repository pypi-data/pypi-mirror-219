"""file/image gallery view

:organization: Logilab
:copyright: 2006-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

__docformat__ = "restructuredtext en"

from logilab.mtconverter import xml_escape

from cubicweb_web.view import EntityView
from cubicweb.predicates import is_instance, has_mimetype, adaptable
from cubicweb_web.views import ajaxcontroller
from cubicweb_web import NotFound


class GalleryView(EntityView):
    __regid__ = "gallery"
    __select__ = is_instance("File")

    currently_displayed = None

    def call(self):
        self._cw.add_js(("cubes.file.js", "cubicweb.ajax.js"))
        self._cw.add_css("cubes.file.css")
        try:
            eid = int(self._cw.form.get("selected", self.cw_rset[0][0]))
        except ValueError:
            raise NotFound()
        self.currently_displayed = eid
        rset = self._cw.execute("Any X where X eid %(x)s", {"x": eid})
        if not rset:
            raise NotFound()
        for i in range(self.cw_rset.rowcount):
            self.cell_call(row=i, col=0)
        self.w('<div id="imageholder">')
        self.wview("primary", rset, row=0, col=0, initargs={"is_primary": False})
        self.w("</div>")
        self.w('<div class="imagegallery">')
        self.w("</div>")

    def cell_call(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        ithumb = entity.cw_adapt_to("IThumbnail")
        if ithumb is not None:
            icon = xml_escape(ithumb.thumbnail_url())
        else:
            icon = self._cw.uiprops["FILE_ICON"]
        title = xml_escape(entity.dc_title())
        # .currently_displayed is None if we went directly to cell_call,
        # eg view called only for that entity, in which case we want
        # it to be considered as selected.
        if self.currently_displayed is None or entity.eid == self.currently_displayed:
            self.w(
                '<a href="javascript:displayImg(%(eid)s)" title="%(title)s"><img id="img%(eid)s" '
                'class="selectedimg" alt="%(title)s" src="%(icon)s"/></a>'
                % {"eid": entity.eid, "title": title, "icon": icon}
            )
        else:
            self.w(
                '<a href="javascript:displayImg(%(eid)s)" title="%(title)s"><img id="img%(eid)s" '
                'alt="%(title)s" src="%(icon)s"/></a>'
                % {"eid": entity.eid, "title": title, "icon": icon}
            )


@ajaxcontroller.ajaxfunc(output_type="xhtml")
def get_image(self, eid):
    return self._cw.view(
        "primary", self._cw.eid_rset(eid), row=0, col=0, initargs={"is_primary": False}
    )


class AlbumView(EntityView):
    __regid__ = "album"
    __select__ = adaptable("IImage")  # good enough for IThumbnail

    def call(self, nbcol=5):
        self._cw.add_css("cubes.file.css")
        lines = [[]]
        for idx in range(self.cw_rset.rowcount):
            if len(lines[-1]) == nbcol:
                lines.append([])
            lines[-1].append(self._make_cell(idx, 0))
        while len(lines[-1]) != nbcol:
            lines[-1].append("&#160;")
        self.w('<table class="album">')
        for line in lines:
            self.w("<tr>")
            self.w("".join(f"<td>{cell}</td>" for cell in line))
            self.w("</tr>")
        self.w("</table>")

    def _make_cell(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        icon = xml_escape(entity.cw_adapt_to("IThumbnail").thumbnail_url())
        title = xml_escape(entity.dc_title())
        return (
            '<a href="%(url)s" title="%(title)s"><img alt="%(title)s" src="%(icon)s"/></a>'
            % {"url": xml_escape(entity.absolute_url()), "title": title, "icon": icon}
        )

    def cell_call(self, row, col):
        self.w(self._make_cell(row, col))


class ImageAdaptedView(AlbumView):
    __regid__ = "sameetypelist"
    __select__ = has_mimetype("image/") & adaptable("IImage")
