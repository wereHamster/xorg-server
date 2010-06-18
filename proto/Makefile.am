
noinst_LTLIBRARIES = libproto.la

INCLUDES = @XORG_INCS@ -I..
AM_CFLAGS = $(DIX_CFLAGS)

SRCS =

if DPMSExtension
SRCS += dpms.h dpms.c dpms-impl.c
endif

libproto_la_SOURCES = $(SRCS)
