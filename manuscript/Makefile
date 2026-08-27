.PHONY: split network pulse methods clean-split

split: network pulse methods

network:
	$(MAKE) -C network-root-transfer paper

pulse:
	$(MAKE) -C pulse-threshold paper

methods:
	$(MAKE) -C rfde-methods-notes paper

clean-split:
	$(MAKE) -C network-root-transfer clean
	$(MAKE) -C pulse-threshold clean
	$(MAKE) -C rfde-methods-notes clean
