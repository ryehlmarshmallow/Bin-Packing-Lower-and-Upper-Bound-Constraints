SRCDIR_CXX = src/cpp
SRCDIR_PY = src/py
DISTDIR = dist

CXX = g++
CXXFLAGS = -Wall -std=c++17 -O2 -march=native

CXX_SOURCES = $(wildcard $(SRCDIR_CXX)/*.cpp)
CXX_EXECUTABLES = $(patsubst $(SRCDIR_CXX)/%.cpp,$(DISTDIR)/%,$(CXX_SOURCES))
PY_SOURCES = $(wildcard $(SRCDIR_PY)/*.py)
PY_DEST = $(patsubst $(SRCDIR_PY)/%.py,$(DISTDIR)/%.py,$(PY_SOURCES))

all: $(DISTDIR) $(CXX_EXECUTABLES) $(PY_DEST)

$(DISTDIR):
	mkdir -p $@

$(DISTDIR)/%: $(SRCDIR_CXX)/%.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

$(DISTDIR)/%.py: $(SRCDIR_PY)/%.py
	cp $< $@

clean:
	rm -rf $(DISTDIR)

.PHONY: all clean