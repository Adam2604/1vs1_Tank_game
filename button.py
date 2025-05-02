class Button:
	def __init__(self, image, position, label, font, normal_color, hover_color):
		self.image = image
		self.position = position
		self.font = font
		self.label_text = label
		self.normal_color = normal_color
		self.hover_color = hover_color

		self.text_surface = self.font.render(self.label_text, True, self.normal_color)

		if self.image is None:
			self.image = self.text_surface

		self.image_rect = self.image.get_rect(center=self.position)
		self.text_rect = self.text_surface.get_rect(center=self.position)

	def draw(self, screen):
		screen.blit(self.image, self.image_rect)
		screen.blit(self.text_surface, self.text_rect)

	def is_clicked(self, mouse_pos):
		return self.image_rect.collidepoint(mouse_pos)

	def update_color(self, mouse_pos):
		color = self.hover_color if self.image_rect.collidepoint(mouse_pos) else self.normal_color
		self.text_surface = self.font.render(self.label_text, True, color)