import pyfpdf.fpdf

pdf = pyfpdf.fpdf.FPDF(format = "letter")
pdf.add_page()
pdf.set_font("Arial", size=12)
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec est justo, porta eu facilisis ac, hendrerit sit amet nunc. Maecenas lobortis nibh orci, eget fringilla diam mattis quis. Phasellus vel lorem sed velit vulputate pharetra et in justo. Nulla vel est ut erat eleifend placerat. Nam non sapien leo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Duis a lacinia magna. Nullam malesuada tincidunt tortor. Integer iaculis, dui at condimentum ornare, dolor leo convallis tortor, at egestas mi metus vel tellus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aliquam pharetra, eros ac ullamcorper tempus, felis est consectetur ligula, vitae gravida ex tellus eget lectus. Sed interdum dolor nibh, quis ullamcorper odio facilisis vel. Suspendisse semper arcu est, quis malesuada elit tempor aliquam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam erat volutpat."
#pdf.cell(0, txt=text, align="C")
pdf.write(h= 10, txt= text)
pdf.output("tutorial.pdf")