
noinst_LTLIBRARIES = libproto.la

INCLUDES = @XORG_INCS@ -I..
AM_CFLAGS = $(DIX_CFLAGS)

SRCS =

if DPMSExtension
SRCS += dpms.c dpms.h dpms-impl.h
endif

libproto_la_SOURCES = $(SRCS)
