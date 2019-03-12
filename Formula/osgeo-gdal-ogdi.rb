class OsgeoGdalOgdi < Formula
  desc "GDAL/OGR 2.x plugin for OGDI driver"
  homepage "http://www.gdal.org/drv_ogdi.html"
  url "http://download.osgeo.org/gdal/2.4.0/gdal-2.4.0.tar.gz"
  sha256 "a568cf3dc7bb203ae12a48e1eb2a42302cded499ef6eccaf9e8f09187d8ce75a"

  revision 1

  head "https://github.com/OSGeo/gdal.git", :branch => "master"

  depends_on "osgeo-ogdi"
  depends_on "osgeo-gdal"

  def gdal_majmin_ver
    gdal_ver_list = Formula["osgeo-gdal"].version.to_s.split(".")
    "#{gdal_ver_list[0]}.#{gdal_ver_list[1]}"
  end

  def gdal_plugins_subdirectory
    "gdalplugins/#{gdal_majmin_ver}"
  end

  def install
    ENV.cxx11
    ogdi_opt = Formula["osgeo-ogdi"].opt_prefix

    gdal_plugins = lib/gdal_plugins_subdirectory
    gdal_plugins.mkpath
    # (HOMEBREW_PREFIX/"lib/#{gdal_plugins_subdirectory}").mkpath

    # add external plugin registration
    inreplace "#{Dir.pwd}/ogr/ogrsf_frmts/ogdi/ogrogdi.h",
              %r{(#endif /\* OGDOGDI_H_INCLUDED \*/)},
              <<~EOS

              CPL_C_START
              void CPL_DLL RegisterOGROGDI();
              CPL_C_END

              \\1
              EOS

    # cxx flags
    args = %W[-Iport -Igcore -Iogr -Iogr/ogrsf_frmts -Iogr/ogrsf_frmts/generic
              -Iogr/ogrsf_frmts/ogdi -I#{ogdi_opt}/include/ogdi]

    # source files
    Dir["ogr/ogrsf_frmts/ogdi/*.c*"].each do |src|
      args.concat %W[#{src}]
    end

    # plugin dylib
    dylib_name = "ogr_OGDI.dylib"
    args.concat %W[
      -dynamiclib
      -install_name #{opt_lib}/#{gdal_plugins_subdirectory}/#{dylib_name}
      -current_version #{version}
      -compatibility_version #{gdal_majmin_ver}.0
      -o #{gdal_plugins}/#{dylib_name}
      -undefined dynamic_lookup
    ]

    # ld flags
    args.concat %W[-L#{ogdi_opt}/lib/ogdi -logdi]

    # build and install shared plugin
    system ENV.cxx, *args
  end

  def caveats; <<~EOS
    This formula provides a plugin that allows GDAL or OGR to access geospatial
    data stored in its format. In order to use the shared plugin, you may need
    to set the following enviroment variable:

      export GDAL_DRIVER_PATH=#{HOMEBREW_PREFIX}/lib/gdalplugins
  EOS
  end

  test do
    ENV["GDAL_DRIVER_PATH"] = "#{HOMEBREW_PREFIX}/lib/gdalplugins"
    gdal_opt_bin = Formula["osgeo-gdal"].opt_bin
    out = shell_output("#{gdal_opt_bin}/ogrinfo --formats")
    assert_match "OGR_OGDI -vector- (ro): OGDI Vectors (VPF, VMAP, DCW)", out
  end
end