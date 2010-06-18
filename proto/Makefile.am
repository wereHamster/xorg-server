
noinst_LTLIBRARIES = libproto.la

INCLUDES = @XORG_INCS@ -I..
AM_CFLAGS = $(DIX_CFLAGS)

SRCS =

if XCB
SRCS += dpms.c
endif

libproto_la_SOURCES = $(SRCS)
